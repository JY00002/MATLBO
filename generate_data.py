import os
import sys
import argparse
import json
import numpy as np
from rl4co.data.utils import check_extension
from rl4co.utils.pylogger import get_pylogger

try:
    import yaml
except ImportError:
    yaml = None

log = get_pylogger(__name__)

def load_config(config_path):
    ext = os.path.splitext(config_path)[1].lower()
    with open(config_path, 'r') as f:
        if ext == '.json':
            config = json.load(f)
        elif ext in ('.yaml', '.yml'):
            if yaml is None:
                raise ImportError("PyYAML is required to load YAML files. Please install it or use JSON.")
            config = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file format: {ext}. Use .json or .yaml")
    return config


def generate_env_data(env_type, *args, **kwargs):
    try:
        args = [arg for arg in args if arg is not None]
        return getattr(sys.modules[__name__], f"generate_{env_type}_data")(
            *args, **kwargs
        )
    except AttributeError:
        raise NotImplementedError(f"Environment type {env_type} not implemented")


def generate_hdsstp_data(
        dataset_size,
        graph_size,
        num_agents=5,
        min_loc=0.0,
        max_loc=1.0,
        min_range=5.0,
        max_range=10.0,
        min_speed=0.5,
        max_speed=1.0,
        min_service_time=1.0,
        max_service_time=5.0,
        num_drone_types=3,
        drone_capabilities=None,
        min_turning_radius=0.005,
        max_turning_radius=0.015
):
    """
    Parameters:
    dataset_size (int): Number of instances to generate
    graph_size (int): Number of targets (customers)
    num_agents (int): Number of drones (agents), must be a multiple of num_drone_types
    min_loc (float): Minimum value for location coordinates
    max_loc (float): Maximum value for location coordinates
    min_range (float): Minimum range capacity for drones
    max_range (float): Maximum range capacity for drones
    min_speed (float): Minimum speed for drones
    max_speed (float): Maximum speed for drones
    min_service_time (float): Minimum service time for subtasks
    max_service_time (float): Maximum service time for subtasks
    num_drone_types (int): Number of drone types (default is 3)
    drone_capabilities: Drone capability matrix of shape [num_drone_types, num_task_types]
    min_turning_radius (float): Minimum turning radius for drones
    max_turning_radius (float): Maximum turning radius for drones

    Returns:
    dict: A dictionary containing generated data arrays for:
        - locs: target locations [dataset_size, graph_size, 2]
        - depot: depot location [dataset_size, 2]
        - speed: speed for each UAV [dataset_size, num_agents]
        - drone_capabilities: UAV capability matrix [dataset_size, num_drone_types, num_drone_types]
        - turning_radii: turning radii for each UAV [dataset_size, num_agents]
    """

    locs = np.random.uniform(min_loc, max_loc, size=(dataset_size, graph_size, 2))

    depot = np.random.uniform(min_loc, max_loc, size=(dataset_size, 2))

    base_pattern = [i % num_drone_types for i in range(num_agents)]
    drone_types = np.tile(base_pattern, (dataset_size, 1))

    range_vals = np.random.uniform(min_range, max_range, size=(dataset_size, num_agents))
    speed = np.random.uniform(min_speed, max_speed, size=(dataset_size, num_agents))

    turning_radii = np.random.uniform(
        min_turning_radius, max_turning_radius, size=(dataset_size, num_agents)
    )

    service_times = np.random.uniform(
        min_service_time, max_service_time, size=(dataset_size, num_drone_types)
    )
    service_times = np.clip(service_times, min_service_time, max_service_time)

    service_time_matrix = np.repeat(
        service_times[:, np.newaxis, :], graph_size, axis=1
    ).reshape(dataset_size, graph_size * 3)

    if drone_capabilities is not None:
        capabilities = np.tile(drone_capabilities, (dataset_size, 1, 1))
    else:
        default_capabilities = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ], dtype=bool)
        capabilities = np.tile(default_capabilities, (dataset_size, 1, 1))

    data = {
        "locs": locs.astype(np.float32),
        "depot": depot.astype(np.float32),
        "drone_types": drone_types.astype(np.int64),
        "range_vals": range_vals.astype(np.float32),
        "speed": speed.astype(np.float32),
        "turning_radii": turning_radii.astype(np.float32),
        "service_times": service_time_matrix.astype(np.float32),
        "drone_capabilities": capabilities.astype(bool),
    }

    return data


def generate_dataset(
        filename=None,
        data_dir="data",
        name=None,
        problem="hdsstp",
        dataset_size=100,
        graph_sizes=None,
        overwrite=False,
        seed=1234,
        disable_warning=True,
        **kwargs,
):

    if graph_sizes is None:
        graph_sizes = [128, 256]
    if isinstance(graph_sizes, int):
        graph_sizes = [graph_sizes]
    for graph_size in graph_sizes:
        datadir = os.path.join(data_dir, problem)
        os.makedirs(datadir, exist_ok=True)

        if filename is None:
            fname = os.path.join(
                datadir,
                "{}{}_seed{}.npz".format(
                    graph_size,
                    "_{}".format(name) if name is not None else "",
                    seed,
                ),
            )
        else:
            fname = check_extension(filename, extension=".npz")

        if not overwrite and os.path.isfile(check_extension(fname, extension=".npz")):
            if not disable_warning:
                log.info(
                    "File {} already exists! Run with -f option to overwrite. Skipping...".format(
                        fname
                    )
                )
            continue

        np.random.seed(seed)

        dataset = generate_env_data(problem, dataset_size, graph_size, **kwargs)

        # A function can return None in case of an error or a skip
        if dataset is not None:
            # Save to disk as dict
            log.info("Saving {} dataset to {}".format(problem, fname))
            np.savez(fname, **dataset)


def generate_with_drones(problem, size_drones_dict, **kwargs):
    for graph_size, num_agents_list in size_drones_dict.items():
        for num_agents in num_agents_list:
            kwargs["num_agents"] = num_agents

            print(
                "Generating instances: {} N {}, m {}...".format(
                    problem.upper(),
                    graph_size,
                    num_agents,
                )
            )

            # 临时将 graph_size 放入 kwargs 供 generate_dataset 使用
            kwargs["graph_sizes"] = graph_size
            fname = os.path.join(
                kwargs["data_dir"],
                problem,
                "n{}_m{}_seed{}.npz".format(
                    graph_size,
                    num_agents,
                    kwargs["seed"],
                ),
            )

            generate_dataset(problem=problem, filename=fname, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HDSSTP dataset with config file.")
    parser.add_argument("--config", type=str, required=True,
                        help="Path to configuration file (JSON or YAML).")
    args = parser.parse_args()

    config = load_config(args.config)

    problem = config.get("problem", "hdsstp")
    data_dir = config["data_dir"]
    seed = config.get("seed", 1234)
    dataset_size = config.get("dataset_size", 50)

    size_drones_dict_raw = config["size_drones_dict"]
    size_drones_dict = {int(k): v for k, v in size_drones_dict_raw.items()}

    exclude_keys = {"problem", "data_dir", "seed", "dataset_size", "size_drones_dict"}
    gen_kwargs = {k: v for k, v in config.items() if k not in exclude_keys}
    gen_kwargs.update({
        "data_dir": data_dir,
        "seed": seed,
        "dataset_size": dataset_size,
    })

    print(f"Generating instances for {problem.upper()} using config: {args.config}")
    generate_with_drones(problem, size_drones_dict, **gen_kwargs)