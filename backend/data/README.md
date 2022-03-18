## Scripts

- Used for generating user, voter, polling, voting, department data
When we need to reset the database due to e.g., change in model structure,
we'll have to update the scripts.

All you need is pandas for the main `py_generator`. `pip install pandas`.

### Generate Scripts Order

Right now, `gen_data.py` is not implemented.
To manually generate data, run the scripts in the following order:

- `gen_departments.py`
- `gen_vote.py`
- `gen_contribution_benefits.py`
- `gen_users.py`
