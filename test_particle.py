import unittest
import numpy as np

from particle import Particle

class TestParticleClass(unittest.TestCase):

    def test_set_position_cart_to_pol(self):
        
        test_particle = Particle(mass=1)
        # first case
        # ----------
        test_particle.set_position(position=np.array([1,1])
                                            , coord_sys='cartesian')
        expected_r = np.sqrt(2)
        expected_theta = np.pi / 4
        self.assertEqual(expected_r, test_particle.r)
        self.assertEqual(expected_theta, test_particle.theta)
        # second case
        # ----------
        test_particle.set_position(position=np.array([1,-1])
                                            , coord_sys='cartesian')
        expected_r = np.sqrt(2)
        expected_theta = 2*np.pi - np.pi / 4
        self.assertEqual(expected_r, test_particle.r)
        self.assertEqual(expected_theta, test_particle.theta)
        # third case
        # ----------
        test_particle.set_position(position=np.array([-3,-4])
                                            , coord_sys='cartesian')
        expected_r = 5
        expected_theta = np.arctan(4/3) + np.pi
        self.assertAlmostEqual(expected_r, test_particle.r, 10)
        self.assertAlmostEqual(expected_theta, test_particle.theta, 10)

    def test_position_cart_origo(self):
        '''
            Tests when cartesian coordinates are set to (0,0)
        '''
        test_particle = Particle(mass=1)
        # first case
        # ----------
        test_particle.set_position(position=np.array([0, 0])
                                            , coord_sys='cartesian')
        with self.assertRaises(AttributeError):
            test_particle.r
        with self.assertRaises(AttributeError):
            test_particle.theta

    def test_set_position_pol_to_cart(self):

        test_particle = Particle(mass=1)
        # first case
        # -----------
        test_particle.set_position(position=np.array([1, np.pi / 4])
                                            , coord_sys='polar')
        expected_x = 1 / np.sqrt(2)
        expected_y = 1 / np.sqrt(2)
        self.assertAlmostEqual(expected_x, test_particle.x, places=10)
        self.assertAlmostEqual(expected_y, test_particle.y, places=10)
        # second case
        # -----------
        test_particle.set_position(position=np.array([1, 3 * np.pi /4])
                                            , coord_sys='polar')
        expected_x = - 1 / np.sqrt(2)
        expected_y = 1 / np.sqrt(2)
        self.assertAlmostEqual(expected_x, test_particle.x, places=10)
        self.assertAlmostEqual(expected_y, test_particle.y, places=10)
        # third case
        # ----------
        with self.assertRaises(ValueError):
            test_particle.set_position(position=np.array([0, np.pi / 2])
                                                , coord_sys='polar')    
        
    def test_set_velocity_cart_to_pol(self):

        test_particle = Particle(mass=1)
        # first case
        # ----------
        test_particle.set_position(position=np.array([1 / np.sqrt(2)
                                                      , 1 / np.sqrt(2)])
                                            , coord_sys='cartesian')
        
        test_particle.set_velocity(velocity=np.array([np.sqrt(2)
                                                      , np.sqrt(2)])
                                            , coord_sys='cartesian')
        expected_vr = 2
        expected_w= 0
        self.assertAlmostEqual(expected_vr, test_particle.vr, 10)
        self.assertAlmostEqual(expected_w, test_particle.w, 10)
        # second case
        # ----------
        test_particle.set_position(position=np.array([1 / np.sqrt(2)
                                                      , 1 / np.sqrt(2)])
                                            , coord_sys='cartesian')
        
        test_particle.set_velocity(velocity=np.array([-np.sqrt(2)
                                                      , np.sqrt(2)])
                                            , coord_sys='cartesian')
        expected_vr = 0
        expected_w= 2
        self.assertAlmostEqual(expected_vr, test_particle.vr, 10)
        self.assertAlmostEqual(expected_w, test_particle.w, 10)
            
    def test_set_velocity_pol_to_cart(self):

        test_particle = Particle(mass=1)
        # first case
        # ----------
        test_particle.set_position(position=np.array([1, np.pi / 2])
                                            , coord_sys='polar')
        
        test_particle.set_velocity(velocity=np.array([2, 0])
                                            , coord_sys='polar')
        expected_vx = 0
        expected_vy= 2
        self.assertAlmostEqual(expected_vx, test_particle.vx, 10)
        self.assertAlmostEqual(expected_vy, test_particle.vy, 10)
        # second case
        # ----------
        test_particle.set_position(position=np.array([1, 0])
                                            , coord_sys='polar')
        
        test_particle.set_velocity(velocity=np.array([2, 0])
                                            , coord_sys='polar')
        expected_vx = 2
        expected_vy= 0
        self.assertAlmostEqual(expected_vx, test_particle.vx, 10)
        self.assertAlmostEqual(expected_vy, test_particle.vy, 10)
        # third case
        # ----------
        test_particle.set_position(position=np.array([1, np.pi / 2])
                                            , coord_sys='polar')
        
        test_particle.set_velocity(velocity=np.array([0, 3])
                                            , coord_sys='polar')
        expected_vx = -3
        expected_vy= 0
        self.assertAlmostEqual(expected_vx, test_particle.vx, 10)
        self.assertAlmostEqual(expected_vy, test_particle.vy, 10)
        # fourth case
        # ----------
        test_particle.set_position(position=np.array([2, np.pi])
                                            , coord_sys='polar')
        
        test_particle.set_velocity(velocity=np.array([0, 3])
                                            , coord_sys='polar')
        expected_vx = 0
        expected_vy= -6
        self.assertAlmostEqual(expected_vx, test_particle.vx, 10)
        self.assertAlmostEqual(expected_vy, test_particle.vy, 10)



if __name__=='__main__':
    unittest.main()