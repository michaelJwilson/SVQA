import  os
import  glob
import  random
import  numpy                  as      np
import  pylab                  as      pl
import  matplotlib.pyplot      as      plt
import  astropy.io.fits        as      fits
import  astropy.units          as      u
import  healpy                 as      hp

from    astropy.table          import  Table, join, hstack
from    astropy                import  constants as const
from    desitarget.geomask     import  circles
from    desiutil.bitmask       import  BitMask
from    desitarget.targetmask  import  load_mask_bits
from    astropy.coordinates    import  SkyCoord
from    astropy                import  units     as u
from    desimodel.footprint    import  pix2tiles, find_tiles_over_point, is_point_in_desi
from    desitarget.targets     import  encode_targetid


##  https://faun.rc.fas.harvard.edu/eschlafly/desi/tiling/dr8/note.pdf
##  AIRMASS:        Airmass if observed 15. deg. from transit.
##  STAR_DENSITY:   Median # of GAIA stars with G < 19.5 per sq. deg. in tile. 
##  IMAGEFRAC R:    Fraction of this tile within 1.605 deg. of r imaging.     
##  IMAGEFRAC GRZ:  Fraction of this tile within 1.605 deg. of grz imaging. 
_file      = fits.open('/global/cscratch1/sd/mjwilson/BGS/SV-ASSIGN/tiles/BGS_SV_30_3x_superset60_Sep2019.fits')
tiles      = Table(_file[1].data)['AIRMASS', 'STAR_DENSITY', 'IMAGEFRAC_R', 'IMAGEFRAC_GRZ', 'TILEID', 'RA', 'DEC']

##
scratch    = os.environ['CSCRATCH']
_sv_mtl    = fits.open(scratch + '/BGS/SV-ASSIGN/mtls/MTL_ALLBGS_STDFAINT_STDBRIGHT_svresolve.0.31.0_49677629_samePRIORITY.fits')
sv_mtl     = Table(_sv_mtl[1].data)

##
sv_mtl['TARGETID'] = encode_targetid(objid=sv_mtl['BRICK_OBJID'], brickid=sv_mtl['BRICKID'], release=sv_mtl['RELEASE'], sky=0, mock=0)
sv_mtl.pprint()

sv_mtl.write(scratch + '/BGS/SV-ASSIGN/mtls/MTL_ALLBGS_STDFAINT_STDBRIGHT_svresolve.0.31.0_49677629_samePRIORITY.fits', format='fits', overwrite=True)

##
nside      = 64

(indesi, tindex)          = is_point_in_desi(tiles, sv_mtl['RA'].quantity.value, sv_mtl['DEC'].quantity.value, return_tile_index=True)

##  Prevent 'duplication' of e.g. RA cols after join. 
del tiles['RA']
del tiles['DEC']

##  Some objects in the .mtl are not in the tiles;  rough cut on creation I guess. 
sv_mtl['TILEID']          = -99 * np.ones_like(sv_mtl['RA'].quantity.value, dtype=np.int)
sv_mtl['TILEID'][indesi]  = tiles['TILEID'].quantity[tindex[indesi]]
sv_mtl.sort('TILEID')
  
##  Not associated to a tile?
##  notin = sv_mtl[sv_mtl['TILEID'] < 0]
##  notin.sort('DEC')
##  print(notin)

##  pl.plot(notin['RA'], notin['DEC'], c='k', marker='.', lw=0, markersize=1)
##  pl.show()

##  Only keep the targets in a given tile. 
sv_mtl     = sv_mtl[sv_mtl['TILEID'] > 0]
sv_mtl     = join(sv_mtl, tiles, keys=['TILEID'], join_type='left')

##  Unique TILEIDS.
utiles     = np.unique(sv_mtl['TILEID'].quantity)

for ii, _tile in enumerate(utiles):
  print('Solving for {} of {}.'.format(ii, len(utiles)))

  fname    = scratch + '/BGS/SV-ASSIGN/svmtl_{:06d}.fits'.format(_tile)
  tile_cut = sv_mtl[sv_mtl['TILEID'] == _tile]

  print(tile_cut)
  
  tile_cut.write(fname, format='fits', overwrite=True)

print('\n\nDone.\n\n')
