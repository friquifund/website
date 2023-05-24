import os

from src.tasks.linkedin_parse.lib.etl import preprocess_members, postprocess_web_data, preprocess_csv_web
from src.tasks.linkedin_parse.lib.filter import get_eligible_profiles
from src.tasks.linkedin_parse.lib.linkedin_sel import Linkedin
from src.utils.connectors.gspreadsheets import Gspread
from src.utils.datasets.load import load_in_memory
from src.utils.datasets.save import save_to_disk
from src.utils.initialization import initialize_run


def task_parse_linkedin(config, log):

    # Load raw data
    log.info("Loading: Start")
    # Load members information from google spreadsheet file
    gc = Gspread(config.credentials.google)
    df_spreadsheet_members = gc.read_spreadsheet(
        url=config.datasets.spreadsheet_members,
        columns=["LinkedIn", "Name", "In Web Page", "status"]
    )
    # Read team data output file, we read it to understand what was the last update date
    df_csv_web = load_in_memory(config.datasets.csv_web)

    df_spreadsheet_members = preprocess_members(df_spreadsheet_members)

    df_csv_web = preprocess_csv_web(df_csv_web)
    # Get profiles eligible for update
    log.info("Looking for eligible profiles: Start")
    df_eligible = get_eligible_profiles(
        df_spreadsheet_members,
        df_csv_web,
        config.parameters.max_profiles_update)
    #profiles_specific = ["David Bofill", "Andreu Mayo", "Martí Mayo Casademont", "Hugo Zaragoza Ballester"]
    profiles_specific = ["Hugo Zaragoza Ballester"]
    df_eligible = df_eligible[df_eligible["name"].isin(profiles_specific)]

    if df_eligible.shape[0] == 0:
        log.warning(
            "No profiles are eligible for update, "
            "either no new profiles or all profiles are already up to date, code will exit")
        return 0
    log.info("Looking for eligible profiles: End")

    # Initialize linkedin class
    log.info("Parsing: Start")

    linkedin = Linkedin(config.credentials.linkedin.user, config.credentials.linkedin.password, config.html_structure)
    linkedin.login()
    df_team_parsed, dict_pictures, df_exceptions = linkedin.parse_profile_multiple(df_eligible)
    log.info("Parsing: End")

    # Postprocess output
    df_team_output = postprocess_web_data(df_csv_web, df_team_parsed, config.parameters.leadership_members)

    log.info("Saving: Start")
    # Update original csv
    save_to_disk(df_team_output, config.datasets.csv_web)

    # Save pictures
    for key, picture in dict_pictures.items():
        save_to_disk(picture["picture_data"], os.path.join(config.datasets.image_folder, picture["picfile"]))
    log.info("Saving: End")


if __name__ == "__main__":
    config, log = initialize_run()
    task_parse_linkedin(config, log)

