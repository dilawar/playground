import moose
import moose.utils as mu

compts_ = {}
tables_ = {}

def add_molecule( name, num ):
    p = moose.Pool( '/compt/%s' % name )
    compts_[name] = p
    p.concInit = num
    t = moose.Table2( '/table%s' % name )
    moose.connect( t, 'requestOut', p, 'getConc' )
    tables_[name] = t
    return p

compt = moose.CubeMesh('/compt')
compt.volume = 1e-3

a = add_molecule( 'a', 1e-5 )
b = add_molecule( 'b', 1e-5 )
c = add_molecule( 'c', 1e-6 )

r = moose.Reac( '/compt/reac' )
r.Kf = 1
r.Kb = 1

moose.connect( r, 'sub', a, 'reac' ) 
# moose.connect( r, 'sub', a, 'reac' ) 
# moose.connect( r, 'sub', b, 'reac' ) 
# moose.connect( r, 'sub', b, 'reac' ) 
moose.connect( r, 'sub', b, 'reac' ) 
moose.connect( r, 'prd', c, 'reac' )

moose.reinit()
moose.start(1)

mu.plotRecords( tables_ )
