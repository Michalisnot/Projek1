from math import sin, cos, sqrt, atan, atan2, degrees, radians, log,tan,pi
# from pprint import pprint
import numpy as np
o = object()
import sys
class Transformacje:
    def __init__(self, model: str = "grs80"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            ecc2 - mimośród^2
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        + Parametry planet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
        """
        if model == "wgs84":
            self.a = 6378137.0 # semimajor_axis
            self.b = 6356752.31424518 # semiminor_axis
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "mars":
            self.a = 3396900.0
            self.b = 3376097.80585952
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) # eccentricity  WGS84:0.0818191910428 
        self.ecc2 = (2 * self.flat - self.flat ** 2) # eccentricity**2


    def r_curv(self,f):
        N = self.a / np.sqrt(1 - self.ecc2 * np.sin(f)**2)
        return (N)
    def xyz2plh(self, X, Y, Z, output = 'dec_degree'):
        """
        Algorytm Hirvonena - algorytm transformacji współrzędnych ortokartezjańskich (x, y, z)
        na współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna (phi, lam, h). Jest to proces iteracyjny. 
        W wyniku 3-4-krotneej iteracji wyznaczenia wsp. phi można przeliczyć współrzędne z dokładnoscią ok 1 cm.     
        Parameters
        ----------
        X, Y, Z : FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        lat
            [stopnie dziesiętne] - szerokość geodezyjna
        lon
            [stopnie dziesiętne] - długośc geodezyjna.
        h : TYPE
            [metry] - wysokość elipsoidalna
        output [STR] - optional, defoulf 
            dec_degree - decimal degree
            dms - degree, minutes, sec
        """
        l = atan2(Y,X)
        p = np.sqrt(X**2 + Y**2)
        f = atan(Z / (p * (1 - self.ecc2)))
        while True:
            N = self.a / np.sqrt(1 - self.ecc2 * np.sin(f)**2)
            h = (p / np.cos(f))- N
            fs = f
            f = np.arctan(Z / (p * (1 - (self.ecc2 * (N / ( N + h))))))
            if np.abs(fs-f) < (0.000001/206265):
                break
        l = np.arctan2(Y,X)
        lat = f
        lon = l
        if output == "dec_degree":
            return degrees(lat), degrees(lon), h 
        elif output == "dms":
            lat = self.deg2dms(degrees(lat))
            lon = self.deg2dms(degrees(lon))
            return f"{lat[0]:02d}:{lat[1]:02d}:{lat[2]:.2f}", f"{lon[0]:02d}:{lon[1]:02d}:{lon[2]:.2f}", f"{h:.3f}"
        else:
            raise NotImplementedError(f"{output} - output format not defined")
    def plh2xyz(self, phi, lam, h):
        """Działanie odwrotne do algorytmu Hirvonena pozwala na transformację z phi, lam, h 
        na współrzędne geocentryczne x,y,z.
        ------
        phi, lam, h :FLOAT 
        współrzędne w układzie geodezyjnym phi i lam w stopniach, h w metrach
        Returns
        -------
        x,y,z:FLOAT 
        współrzędne w układzie geocentrzycznym w metrach"""
       # r = a * sqrt((1 - e2) / 1 - e2 * (np.cos(f) ** 2))
        phi = radians(phi)
        lam = radians(lam)
        
        N = self.a / np.sqrt(1 - self.ecc2 * np.sin(phi)**2)
        # q = Rn*self.ecc2*sin(phi)
        x = (N + h) * np.cos(phi) * np.cos(lam)
        y = (N + h) * np.cos(phi) * np.sin(lam)
        z = (N * (1-self.ecc2) + h) * np.sin(phi)       
        return (x,y,z)        

    #zajęcia 6.05

    def xyz2neu(self,x,y,z,x_0,y_0,z_0):
        """Zamienia układ geocentrzyczny na układ topocentrzyczny """
        phi, lam, _ = [radians(coord) for coord in self.xyz2plh(x,y,z)]
        
        R = np.array([[-sin(lam), -sin(phi)*cos(lam), cos(phi)*cos(lam)],
                      [ cos(lam), -sin(phi)*sin(lam), cos(phi)*sin(lam)],
                      [         0,          cos(phi),          sin(phi)]])
        
        xyz_t = np.array([[x-x_0],
                          [y-y_0],
                          [z-z_0]])
        
        enu = R.T @ xyz_t
        
        return(enu[1],enu[0],enu[2])
        
    
    # def bdl2pdl(self,b,l):
    #     U = 1 + self.ecc2*sin(b)
    #     V = 1 - self.ecc2*sin(b)
    #     K = (U/V)**(self.ecc/2)
    #     C = K * tan(b/2 +pi/4)
    #     phi = 2*atan2(C,1)-pi/2
    #     dl = l
    #     return phi, dl
    # def pdl2xymerc(self, p, dl):
    #     p = sin(p)
    #     q = cos(p)*cos(dl)
    #     r = 1 + cos(p)*sin(dl)
    #     s = 1 - cos(p)*sin(dl)
    #     R0=6367449.14577
    #     x_merc=R0 *atan2(p,q)
    #     y_merc=0.5*R0*log(r/s)
    #     return x_merc, y_merc
    # def xymerc2xygk(self,x_merc,y_merc):
    #     s = 2.0e-6
    #     x_0 = 5760000.000
    #     zz = [(x_merc-x_0)*s,y_merc*s]
    #     a_0 = 5765181.11148097
    #     a_1 = 499800.817138
    #     a_2 = -63.81145283
    #     a_3 = 0.83547915
    #     a_4 = 0.13046891
    #     a_5 = -0.00111138
    #     a_6 = -0.00010504
        
    #     z_gk = [a_0+z*(a_1+z*(a_2+z*(a_3+z*(a_4+z*(a_5+z*(a_6+z)))))) for z in zz]
        
        
        
        
    #     return(z_gk)
    
    # def xygk2xy1992(self,x_gk,y_gk):
    #     m_0 = 0.9993
    #     # x_0 = -5300000
    #     y_0 = 500000
    #     x_1992 = m_0*x_gk+x_0
    #     y_1992 = m_0*y_gk+y_0
    #     return(x_1992,y_1992)
    # def bl2xy1992(self,b,l):
    #     l_0 = radians(19)
    #     dl = l-l_0
    #     p,dl  =  self.bdl2pdl(b, dl)
    #     x_merc, y_merc = self.pdl2xymerc(p, dl)
    #     x_gk, y_gk=  self.xymerc2xygk(x_merc, y_merc)
    #     x_1992,y_1992 =  self.xygk2xy1992(x_gk, y_gk)
    #     return(x_1992,y_1992)
    
    def sigma(self,f):
        """Obliczenie zmiennej do GK """
        a = self.a
        e2  = self.ecc2
        A0 = 1 - e2/4 - 3 * e2**2/64 - 5 * e2**3 / 256
        A2 = (3/8) * (e2 + e2**2 / 4 + 15 * e2**3 / 128)
        A4 = (15/256) * (e2**2 + 3 * e2**3 / 4)
        A6 = 35 * e2**3 / 3072
        sig = a * (A0 * f - A2*np.sin(2*f) + A4*np.sin(4*f) - A6*np.sin(6*f))
        return(sig)
    
    def GK(self,f,l,l0):
        """Zamienia współrzędne f,L na współrzędne w układzie GK x,y o podanym południku odwzorowawczym l0 """
        f = radians(f)
        l = radians(l)
        l0 = radians(l0)
        a = self.a
        e2  = self.ecc2
        b = np.sqrt(a**2 * (1-e2))
        ep2 = (a**2 - b**2)/b**2
        
        dl = l - l0
        t = np.tan(f)
        eta2 = ep2 * np.cos(f)**2
        N = self.r_curv(f)
        
        sig = self.sigma(f)
        
        x_gk = sig + dl**2 / 2 * N * np.sin(f) * np.cos(f) * (1 + dl**2 /    12 * np.cos(f)**2 * (5 - t**2 + 9*eta2 + 4*eta2**2) + dl**4 / 360 * np.cos(f)**4 *(61 - 58*t**2 + t**4 + 270*eta2 - 330*eta2*t**2))
        y_gk = dl*N*np.cos(f)*(1 + dl**2/6*np.cos(f)**2*(1 - t**2 + eta2) + dl**4/120*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*eta2 - 58*eta2*t**2))
        return(x_gk, y_gk)  
    def bl2xy1992(self,b,l,l0=19):
        """Dodaje matryce Ukł. 1992 do obliczonych współrzędnych Gaussa-Krugera """
        x_gk,y_gk = self.GK(b,l,l0)
        m_0 = 0.9993
        x_0 = -5300000
        y_0 = 500000
        x_1992 = m_0*x_gk+x_0
        y_1992 = m_0*y_gk+y_0
        return(x_1992,y_1992)
    def bl2xy00(self,b,l,strefa):
        """Dodaje matryce Ukł. 2000 do obliczonych współrzędnych Gaussa-Krugera """
        x_gk,y_gk = self.GK(b,l,strefa*3)
        m_0 = 0.999923
        y_0 = 500000+strefa*10e6
        x_00 = m_0*x_gk
        y_00 = m_0*y_gk+y_0
        return(x_00,y_00)
if __name__ == "__main__":
    # utworzenie obiektu

    input_file_path = sys.argv[-1]
    # print(sys.argv)
    O = np.shape(sys.argv)
    o = O[0]
    # print(o)
    Model = 'grs80'
    if '-grs80' in sys.argv:
        Model = 'grs80'
    if '-wgs84' in sys.argv:
        Model = 'wgs84'
    geo = Transformacje(model=Model)
    if '-f' in sys.argv:
        i=0
        for j in sys.argv:
            if j == '-f':
                break
            i+=1
        file_name = sys.argv[i+1]
    elif '-r' in sys.argv:
        file_name = 'wsp_xd.txt'
        i=0
        for j in sys.argv:
            if j == '-r':
                break
            i+=1
            # print(i)
        with open('wsp_xd.txt', 'w') as f:
            
            f.write('\n')
            f.write('\n')       
            f.write('\n')      
            f.write('\n')
            if '--plh2xyz' in sys.argv or '--xyz2plh' in sys.argv:
                try:
                    float(sys.argv[i+1])
                    float(sys.argv[i+2])
                    float(sys.argv[i+3])
                except:
                    raise NameError('Podano wartosci w sysytemie innym niz dziesietny')
                f.write(f'{sys.argv[i+1]},{sys.argv[i+2]},{sys.argv[i+3]} \n')
            if '--xyz2neu' in sys.argv:
                try:
                    float(sys.argv[i+1])
                    float(sys.argv[i+2])
                    float(sys.argv[i+3])
                    float(sys.argv[i+4])
                    float(sys.argv[i+5])
                    float(sys.argv[i+6])
                except:
                    raise NameError('Podano wartosci w sysytemie innym niz dziesietny')
                f.write(f'{sys.argv[i+1]},{sys.argv[i+2]},{sys.argv[i+3]},{sys.argv[i+4]},{sys.argv[i+5]},{sys.argv[i+6]}\n')
            
            if '--bl2xy2000' in sys.argv or '--bl2xy1992' in sys.argv:
                try:
                    float(sys.argv[i+1])
                    float(sys.argv[i+2])
                except:
                    raise NameError('Podano wartosci w sysytemie innym niz dziesietny')
                f.write(f'{sys.argv[i+1]},{sys.argv[i+2]}')
    else:raise NameError('Nie podano sposobu dostarczenia danych wejsciowych')
    
    if '--xyz2plh' in sys.argv:
        coords_plh=[]
        with open(f'{file_name}') as f:
            lines = f.readlines()
            lines = lines[4:]
            for line in lines:
                line = line.strip('\n')
                x_str,y_str,z_str= line.split(',')
                x,y,z = (float(x_str),float(y_str),float(z_str))
                p,l,h=geo.xyz2plh(x,y,z)
                coords_plh.append([p,l,h])
        # print(coords_plh)
        with open('Result_xyz2plh.txt', 'w') as f:
            
            f.write('phi[deg],        lambda[deg],          H[m]\n')
            
            
            for coords in coords_plh:
                for coord in coords:
                    if coord != coords[-1]:
                        f.write(f'{coord},')
                    else: f.write(f'{coord}\n')
            
            
    elif '--plh2xyz' in sys.argv:
        coords_xyz=[]
        with open(f'{file_name}') as f:
                lines = f.readlines()
                lines = lines[4:]
                for line in lines:
                    # print(line)
                    line = line.strip('\n')
                    [phi_str,lam_str,h_str]   = line.split(',')
                    phi,lam,h = (float(phi_str),float(lam_str),float(h_str))
                    x,y,z = geo.plh2xyz(phi,lam,h)
                    coords_xyz.append([x,y,z])
            # print(coords_plh)
        with open('Result_plh2xyz.txt', 'w') as f:
            
            f.write('x[m],        y[m],          z[m]\n')
            
            
            for coords in coords_xyz:
                for coord in coords:
                    if coord != coords[-1]:
                        f.write(f'{coord},')
                    else: f.write(f'{coord}\n')            

    elif '--xyz2neu' in sys.argv:
        if '-f' in sys.argv and '-r' in sys.argv:
            for i,s in enumerate(sys.argv):
                if s == '-r':
                    x0 = sys.argv[i+1]
                    y0 = sys.argv[i+2]
                    z0 = sys.argv[i+3]
            
        coords_neu=[]
        with open(f'{file_name}') as f:
            lines = f.readlines()
            lines = lines[4:]
            i=1
            for line in lines:
                line = line.strip('\n')
                xd = line.split(',')
                # if i == 1 and len(xd)!=6:
                    # raise NameError('Nie podano wspolrzędnych x0,y0,z0')
                if len(xd)==6:
                    x_str,y_str,z_str,x0,y0,z0= line.split(',')
                if len(xd)==3:
                    x_str,y_str,z_str = line.split(',')
                x,y,z,x0,y0,z0 = (float(x_str),float(y_str),float(z_str),float(x0),float(y0),float(z0))
                n,e,u=geo.xyz2neu(x,y,z,x0,y0,z0)
                coords_neu.append([n,e,u])
                i=2
        with open('Result_xyz2neu.txt', 'w') as f:
            
            f.write('n[m],        e[m],          u[m]\n')
            
            
            for coords in coords_neu:
                for coord in coords:
                    if coord != coords[-1]:
                        f.write(f'{coord},')
                    else: f.write(f'{coord}\n')    
    elif '--bl2xy1992' in sys.argv:
        coords_92=[]
        with open(f'{file_name}') as f:
            lines = f.readlines()
            lines = lines[4:]
            for line in lines:
                line = line.strip('\n')
                
                bs,ls = line.split(',')
                b,l = (float(bs),float(ls))
                x92,y92=geo.bl2xy1992(b, l)
                
                coords_92.append([x92,y92])
        with open('Result_bl21992.txt', 'w') as f:
            
            f.write('x[m],        y[m]\n')
            
            
            for coords in coords_92:
                for coord in coords:
                    if coord != coords[-1]:
                        f.write(f'{coord},')
                    else: f.write(f'{coord}\n')            
   
    elif '--bl2xy2000' in sys.argv:
        strefa = 0
        coords_00=[]
        with open(f'{file_name}') as f:
            lines = f.readlines()
            lines = lines[4:]
            for line in lines:
                line = line.strip('\n')
                
                bs,ls = line.split(',')
                b,l = (float(bs),float(ls))
                
                if l>=13.5 and l<16.5:
                    strefa = 5
                elif l>=16.5 and l<19.5:
                    strefa = 6
                elif l>=19.5 and l<22.5:
                    strefa = 7
                elif l>=22.5 and l<25.5:
                    strefa = 8
                else: raise NameError('Błędna lambda')
                x00,y00=geo.bl2xy00(b, l, strefa)
                # print(b,l)
                coords_00.append([x00,y00])
        with open('Result_bl2xy2000.txt', 'w') as f:
            
            f.write('x[m],        y[m]\n')
            
            for coords in coords_00:
                for coord in coords:
                    if coord != coords[-1]:
                        f.write(f'{coord},')
                    else: f.write(f'{coord}\n')
    else: raise NameError('Podano nieznaną flagę')
            # coords_plh_line = ','.join([str(coord)for coord in coords])
            
            # coords_00_2= '\n'.join([','.join(str(coord)for coord in coords for coords in coords_00)])
            
            # f.writelines(coords_00_2)   
    # dane XYZ geocentryczne
    # X = 3664940.500; Y = 1409153.590; Z = 5009571.170
    # x0 = 10000; y0 = 5000; z0 = 1000
    
    # phi, lam, h = geo.xyz2plh(X, Y, Z)
    # # print(phi, lam, h)
    # n,e,u = geo.xyz2neu(X, Y, Z, x0, y0, z0)
    # print(n,e,u)


    # coords_plh=[]
# with open('wsp_inp.txt') as f:
#     lines = f.readlines()
#     lines = lines[4:]
#     for line in lines:
#         line = line.strip('\n')
#         x_str,y_str,z_str= line.split(',')
#         x,y,z = (float(x_str),float(y_str),float(z_str))
#         p,l,h=geo.xyz2plh(x,y,z)
#         coords_plh.append([p,l,h])
# print(coords_plh)
# with open('Result_xyz2plh.txt', 'w') as f:
    
#     f.write('phi[deg],        lambda[deg],          H[m]\n')
    
    
#     # coords_plh_line = ','.join([str(coord)for coord in coords])
    
#     coords_plh_line= '\n'.join([str(coords)for coords in coords_plh])
    
#     f.writelines(coords_plh_line)
    
    
# coords_xyz=[]
# with open('Result_xyz2plh.txt') as f:
#         lines = f.readlines()
#         lines = lines[1:]
#         for line in lines:
#             line = line.strip('\n')
#             phi_str,lam_str,h_str = line.split(',')
#             phi,lam,h = (float(x_str),float(y_str),float(z_str))
#             x,y,z = geo.plh2xyz(phi,lam,h)
#             coords_xyz.append([x,y,z])
#     # print(coords_plh)
# with open('Result_plh2xyz.txt', 'w') as f:
    
#     f.write('x[m],        y[m],          z[m]\n')
    
    
#     # coords_plh_line = ','.join([str(coord)for coord in coords])
    
#     coords_xyz_line2= '\n'.join([str(coords)for coords in coords_xyz])
    
#     f.writelines(coords_xyz_line2)
    
    
    
    
    
#zajęcia 6.05

    # def xyz2neu(self,)
    
x,y,z = 1,1,1
x_0,y_0,z_0 = 1,1,3
XD = geo.xyz2neu(x,y,z,x_0,y_0,z_0)    
    

G = geo.bl2xy1992(0.9092689315350225, 0.3670695034002574)

    
    
    
    
    
    
    
    
            