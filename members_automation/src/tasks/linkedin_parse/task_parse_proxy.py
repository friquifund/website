import os
from pathlib import Path

from src.tasks.linkedin_parse.lib.filter import get_eligible_profiles
from src.tasks.linkedin_parse.lib.linkedin_sel import Linkedin
from src.utils.connectors.gspreadsheets import Gspread
from src.utils.datasets.load import load_in_memory
from src.utils.datasets.save import save_to_disk
from src.utils.initialization import initialize_run
from src.tasks.linkedin_parse.lib.etl import preprocess_members, postprocess_web_data


def task_parse_linkedin(config, log):

    # Load raw data
    log.info("Loading: Start")
    # Load members information from google spreadsheet file
    gc = Gspread(config.credentials.google)
    df_spreadsheet_members = gc.read_spreadsheet(
        url=config.datasets.spreadsheet_members,
        columns=["LinkedIn", "Name", "picfile"]
    )
    list_proxy_api_keys = list(gc.read_spreadsheet(
        url=config.datasets.spreadsheet_api,
        columns=["api_key_id"])["api_key_id"])

    # Read team data output file, we read it to understand what was the last update date
    df_csv_web = gc.read_spreadsheet(
        url=config.datasets.spreadsheet_team,
        columns=["name", "linkedin", "city", "title", "picfile", "leadership", "last_updated"])
    log.info("Loading: End")

    df_spreadsheet_members = preprocess_members(df_spreadsheet_members)
    # Get profiles eligible for update
    log.info("Looking for eligible profiles: Start")
    df_eligible = get_eligible_profiles(
        df_spreadsheet_members,
        df_csv_web,
        config.parameters.max_profiles_update)
    profiles_specific = ["David Bofill", "Andreu Mayo", "Martí Mayo Casademont", "Hugo Zaragoza Ballester"]
    #profiles_specific = ["Hugo Zaragoza Ballester"]
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
    # Update spreadhseet in google drive
    gc.write_spreadsheet(df_team_output, )
    # Update original csv
    save_to_disk(df_team_output, config.datasets.csv_web)

    # Save pictures
    for key, picture in dict_pictures.items():
        save_to_disk(picture["picture_data"], os.path.join(config.datasets.image_folder, picture["picfile"]))
    log.info("Saving: End")


if __name__ == "__main__":

    # Crear conta alternativa de linkedin i provar de fer el parsing

    # Step 1, Create file in google drive that will be empty
    # Process will take data from manual file and completely paste it into web_profiles
    # Process will fill profiles that don't have picfile or position or are last updated and get picture and role
    # Step 1 - Find profiles without picfile
    # Update el fitxer per a que nomes contingui la informacio que ens interessa
    # Opcio 2 - Actualitzar perfils antics
    config, log = initialize_run()
    task_parse_linkedin(config, log)


