# Copies all the relevant .csv to postgres
# $1 - '--in' -> copies generated_data to database
#      '--dump' -> copies database to generated_data
# If not specified, will copy to database

# NOTES:
# must first copy all the 'lesser data'
# then copy all the 'upper data' that relies on the lesser data
# Method: COPY [Table/Query] to '[Absolute Path/filename.csv]' csv header;
DATADIR=generated_data/
FUNC=''

if [ $1 = '--dump'] then
    $FUNC="TO"
else
    $FUNC="FROM"
fi

copy_func() {
    psql -u postgres -h localhost <<< COPY $2 $FUNC $DATADIR$1 DELIMITER ',' CSV HEADER;
}

# NEED TO: specify the ids, ensure to regularly clear-data
# Need to also check that all columns are in the same order
# LESSER
copy_func 'departments.csv' api_department
copy_func 'countries.csv' api_country
copy_func 'benefits.csv' api_benefit
copy_func 'interests.csv' api_interest
copy_func 'skills.csv' api_skill
copy_func 'occupations.csv' api_occupation
copy_func 'pollresults.csv' api_localdepartment
copy_func 'pollresults.csv' api_statedepartment
copy_func 'policy_type.csv' api_policytype
copy_func 'initiative.csv' api_initiative 
copy_func 'elections.csv' api_election

# UPPER
copy_func 'voters.csv' api_voter
copy_func 'users.csv' api_user
copy_func 'votes.csv' api_voter
copy_func 'polls.csv' api_poll
copy_func 'pollresults.csv' api_pollresult
