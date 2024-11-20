import gather_functions

if __name__ == "__main__":

    # Create threads for team_stat_pull and team_standing_pull
    #stat_thread = threading.Thread(target=gather_functions.team_stat_pull)
    #standing_thread = threading.Thread(target=gather_functions.team_standing_pull)

    # Start the threads
    #stat_thread.start()
    #standing_thread.start()

    # Wait for both threads to complete
    #stat_thread.join()
    #standing_thread.join()

    # Execute the final function
    #combine_csv_files()

    gather_functions.team_stat_pull(2021,2024)