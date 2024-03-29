# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.dt = params.dt
        self.q = params.q
        self.dim_state = params.dim_state
        

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        
        dim_half = int(self.dim_state / 2)
        
        F = np.identity(self.dim_state)
        F[0:dim_half, dim_half:self.dim_state] = np.identity(dim_half)*self.dt
        

        return np.matrix(F)
    
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############

        dim_half = int(self.dim_state / 2)
        
        dt_pow_three = np.power(self.dt, 3)/3
        dt_pow_two = np.power(self.dt, 2)/2
        
        Q = np.zeros([self.dim_state, self.dim_state])
        
        Q[0:dim_half, 0:dim_half] = np.identity(dim_half)*dt_pow_three*self.q
        Q[0:dim_half, dim_half:self.dim_state] = np.identity(dim_half)*dt_pow_two*self.q
        Q[dim_half:self.dim_state, 0:dim_half] = np.identity(dim_half)*dt_pow_two*self.q
        Q[dim_half:self.dim_state, dim_half:self.dim_state] = np.identity(dim_half)*self.dt*self.q
        
        #print(Q)
        
        return np.matrix(Q)
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        
        
        x_predict = self.F() * track.x
        p_predict = self.F() * track.P * self.F().transpose() + self.Q()
        
        track.set_x(x_predict)
        track.set_P(p_predict)
        
        
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        
        
        H = meas.sensor.get_H(track.x)
        gamma = self.gamma(track, meas)
        S = self.S(track, meas, H)
        K = track.P * H.transpose() * np.linalg.inv(S)
        x = track.x + K * gamma
        I = np.identity(self.dim_state)
        P = (I-K*H) * track.P
        
        
        # save x and P in track
        track.set_x(x)
        track.set_P(P)
        
        
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############
        
        gamma_ = meas.z - meas.sensor.get_hx(track.x)

        return gamma_
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############
        
        S_ = (H*track.P*H.transpose()) + meas.R

        return S_
        
        ############
        # END student code
        ############ 