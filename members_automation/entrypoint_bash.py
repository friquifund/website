import src.tasks as tasks
from src.utils.initialization import initialize_run
import click


@click.command()
@click.option("--task_name", type=str)
def run(task_name: str):
    """
    This is the main entry point of the project, a wrapper function that runs a specific task called under string and
    adds config and constants. Any task that is called has to be imported in the __init__.py of the corresponding module
    Parameters
    ----------
    task_name: main that will be called by the run function
    config: path for the config of the pipeline
    log: path of the log for the pipeline

    Returns Nothing
    -------

    """
    config, log = initialize_run()

    main_function = getattr(tasks, task_name)
    main_function(config, log)


if __name__ == "__main__":
    run()
