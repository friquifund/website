import os

from src.tasks.linkedin_parse.lib.filter import get_eligible_profiles
from src.tasks.linkedin_parse.lib.linkedin_soup import parse_profile_multiple
from src.utils.connectors.gspreadsheets import Gspread
from src.utils.datasets.load import load_in_memory
from src.utils.datasets.save import save_to_disk
from src.utils.initialization import initialize_run
from src.tasks.linkedin_parse.lib.etl import preprocess_members, postprocess_web_data, preprocess_csv_web


def task_parse_linkedin(config, log):

    # Load raw data
    log.info("Loading: Start")
    # Load members information from google spreadsheet file
    gc = Gspread(config.credentials.google)
    df_spreadsheet_members = gc.read_spreadsheet(
        url=config.datasets.spreadsheet_members,
        columns=["LinkedIn", "Name", "In Web Page", "status"]
    )
    list_proxy_api_keys = list(gc.read_spreadsheet(
        url=config.datasets.spreadsheet_api,
        columns=["api_key_id"])["api_key_id"])

    # Read team data output file, we read it to understand what was the last update date
    df_csv_web = load_in_memory(config.datasets.csv_web)
    log.info("Loading: End")

    df_spreadsheet_members = preprocess_members(df_spreadsheet_members)
    df_csv_web = preprocess_csv_web(df_csv_web)
    # Get profiles eligible for update
    log.info("Looking for eligible profiles: Start")
    df_eligible = get_eligible_profiles(
        df_spreadsheet_members,
        df_csv_web,
        config.parameters.max_profiles_update)
    #profiles_specific = ["David Bofill", "Andreu Mayo", "Martí Mayo Casademont", "Hugo Zaragoza Ballester"]
    #profiles_specific = "Ariadna Font"
    #df_eligible = df_eligible[df_eligible["Name"].str.contains(profiles_specific)]
    if df_eligible.shape[0] == 0:
        log.warning(
            "No profiles are eligible for update, "
            "either no new profiles or all profiles are already up to date, code will exit")
        return 0
    log.info("Looking for eligible profiles: End")

    # Initialize linkedin class
    log.info("Parsing: Start")

    df_team_parsed, dict_pictures, df_exceptions = parse_profile_multiple(
        df_eligible,
        config.credentials.nubela_api_key,
        config.credentials.serapi_api_key)
    log.info("Parsing: End")

    # Postprocess output
    df_team_output = postprocess_web_data(df_csv_web, df_team_parsed)

    log.info("Saving: Start")
    # Save pictures
    for key, picture in dict_pictures.items():
        path_picfile = os.path.join(config.datasets.image_folder, f"{picture['picfile']}.jpeg")
        picture_content = picture["picture_data"]
        if not os.path.exists(path_picfile) and len(picture) > 0 and not picture_content.startswith(b"<svg xmlns="):
            save_to_disk(picture_content, path_picfile)

    # Update original csv
    save_to_disk(df_team_output, config.datasets.csv_web)
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


