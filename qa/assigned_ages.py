import glob
import random
import numpy             as      np
import pylab             as      pl
import matplotlib.pyplot as      plt
import astropy.io.fits   as      fits
import astropy.units     as      u

from   astropy.table      import  Table, join, hstack
from   astropy            import  constants as const
from   desitarget.geomask import circles


plt.figure(figsize=(5, 5))

tiles      = Table(fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/tiles/BGS_SV_30_3x_superset60_Sep2019.fits')[1].data)

_assigned  = Table(fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/fiberassign/assigned_targets.fits')[1].data)
_assigned.sort('BRICK_OBJID')

  
legacyn  = Table(fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/truth/ages_reduced-north.fits')[1].data)
legacys  = Table(fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/truth/ages_reduced-south.fits')[1].data)

pl.scatter(legacyn['RAJ2000'], legacyn['DEJ2000'], s=1, rasterized=True, alpha=0.5, marker='x', c='k')
pl.scatter(legacys['RAJ2000'], legacys['DEJ2000'], s=1, rasterized=True, alpha=0.5, marker='x', c='k')

for _file in ['ages_reduced-north-standard_074016', 'ages_reduced-north-standard_074033', 'ages_reduced-south-standard_074033']:
  ages     = Table(fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/truth/standard/bytile/{}.fits'.format(_file))[1].data)
  pl.scatter(ages['RA'], ages['DEC'], s=1, rasterized=True, alpha=0.5, marker='.', c='gold')

pl.xlim(220., 216.)
pl.ylim(32., 36.)

pl.xlabel('RA [deg.]')
pl.ylabel('DEC [deg.]')

pl.title('AGES')  
plt.tight_layout()

pl.show()
##  pl.savefig('spec_truth.png')

print('\n\nDone.\n\n')

