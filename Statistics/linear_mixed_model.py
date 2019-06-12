import statsmodels.api as sm
import statsmodels.formula.api as smf

def main():
    data = sm.datasets.get_rdataset( 'dietox', 'geepack' ).data
    print( data )
    md = smf.mixedlm( "Weight ~ Time", data, groups = data[ "Pig" ] )
    mdf = md.fit()
    print( mdf.summary() )

if __name__ == '__main__':
    main()
