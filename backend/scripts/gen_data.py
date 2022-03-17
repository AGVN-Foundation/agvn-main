'''
Runs all scripts to generate data.

Args:
    --no-regeneration -> will not generate data
    --no-insert -> will not insert generated data into database

Each sub-function creates a table.
e.g. -> create tables for each of the following:
    initiative    election    vote    question    poll    department   "contribution benefit"

If simply resetting the database, just run webserver/scripts/reset-db
NOTE: Should be running this minimally, can take up to two hours to completely generate data
'''
import sys
from gen_departments import gen_departments
from gen_contribution_benefits import gen_contribution_benefits
from gen_users import gen_users, gen_voter_details_editable, gen_voter_details_uneditable
from gen_vote import gen_votes, gen_initiatives, gen_elections


if __name__ == '__main__':

    if '--no-regeneration' in sys.argv[1]:
        exit("Did not generate data")

    gen_elections(100)
    gen_initiatives()
    gen_departments()
    gen_votes()
    gen_contribution_benefits()

    gen_voter_details_editable()
    gen_voter_details_uneditable()
    gen_users()

    if not '--no-insert' in sys.argv:
        exec('./copy_to_database.sh')
