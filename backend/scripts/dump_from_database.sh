# Does the reverse of copy_to_database.sh
# Simply dumps all the relevant api_models from Postgres to generated_data in .csv format

DATADIR=generated_data/

dump_data() {
    psql -u postgres -h localhost <<< COPY $2 TO $DATADIR$1 DELIMITER ',' CSV HEADER;
}

# LESSER
dump_data 'departments.csv' api_department
dump_data 'countries.csv' api_country
dump_data 'benefits.csv' api_benefit
dump_data 'interests.csv' api_interest
dump_data 'skills.csv' api_skill
dump_data 'occupations.csv' api_occupation
dump_data 'pollresults.csv' api_local_department
dump_data 'pollresults.csv' api_state_department
dump_data 'policy_type.csv' api_policytype
dump_data 'initiative.csv' api_initiative 

# UPPER
dump_data 'voters.csv' api_voter
dump_data 'users.csv' api_user
dump_data 'votes.csv' api_voter
dump_data 'polls.csv' api_poll
dump_data 'pollresults.csv' api_pollresult