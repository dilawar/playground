import moose
import moose.utils as mu

compts_ = {}
tables_ = {}

def add_molecule( name, num ):
    p = moose.Pool( '/compt/%s' % name )
    p.concInit = num
    t = moose.Table2( '/table%s' % name )
    moose.connect( t, 'requestOut', p, 'getConc' )
    tables_[name] = t
    compts_[name] = p
    return p

compt = moose.CubeMesh('/compt')
compt.volume = 1

a = add_molecule( 'a', 1e-1 )
b = add_molecule( 'b', 2e-1 )
c = add_molecule( 'c', 1e-3 )

r = moose.Reac( '/compt/reac' )
r.Kf = 1
r.Kb = 1

moose.connect( r, 'sub', a, 'reac' ) 
moose.connect( r, 'sub', b, 'reac' ) 
moose.connect( r, 'prd', c, 'reac' )

stoich = moose.Stoich( '/stoich' )
stoich.compartment = compt
solver = moose.Ksolve( '/compt/solver' )
stoich.ksolve = solver
stoich.path = '/compt/##'

moose.reinit()
moose.start(100)

mu.plotRecords( tables_ )
