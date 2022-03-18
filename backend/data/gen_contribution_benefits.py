import pandas as pd


def gen_contribution_benefits():
    '''
    Generate contribution benefits
    '''
    benefits = [
        "30 subsidy",
        "20 sponsorship",
        "20 tax cut",
        "10 fees"
    ]
    df = pd.DataFrame()
    df['benefit'] = benefits

    df.to_csv('generated_data/benefits.csv', index=False)


if __name__ == '__main__':
    gen_contribution_benefits()
