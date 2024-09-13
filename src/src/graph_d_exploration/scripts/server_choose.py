#!/usr/bin/env python3

# s4636216@studenti.unige.it
# 2023, Università degli Studi di Genova, LS2N Ecole Centrale de Nantes

# This node receives all the centroids information from each agent and computes
# the best choice for each one depending on the reward passed and the distance
# from the centroid

import rospy
import actionlib
import numpy as np

from graph_d_exploration.msg import Point2D, ChooseGoalResult, ChooseGoalFeedback, ChooseGoalAction
from constants import INTER_GOAL_DIST

# Initialize list to store chosen coordinates
# Keeping track of the chosen points, which means that they could have not been used
# but they have been published so potentially used   
chosen_coords = []

chosen_coords_with_info = []

# Greedy approach
class ChoosePointsServer:
    def __init__(self,servername):

        self.ServerName_ = '/'+servername+':'
       
        self.r = rospy.Rate(0.5)  # Hz
        # Variable to store the number of goals
        self.i = 0
        self.server = actionlib.SimpleActionServer(
            'choose_points', ChooseGoalAction, self.execute_callback, False)
        self.server.start()
        rospy.loginfo(f'{self.ServerName_} Server started')

    def execute_callback(self, goal):
        #rospy.loginfo(f'{self.ServerName_} Received lists points from client {goal.client_id}')

        result = ChooseGoalResult()
        # Take the result and cast it with the type chosen in the msg
        result.goals = self.select_points(goal.matrix.data, goal.rows)

        rospy.loginfo(f'{self.ServerName_} Chosen goal for the current agent.')
        self.server.set_succeeded(result)

        if self.server.is_preempt_requested():
            rospy.loginfo(f'{self.ServerName_} Goal was preempted')
            self.server.set_preempted()
        elif rospy.is_shutdown():
            rospy.loginfo(f'{self.ServerName_} Node was shutdown')
            self.server.set_aborted()

    def select_points(self, matrix_, num_rows):
        #rospy.loginfo(f"{self.ServerName_} chosen_coords before assignment : {chosen_coords}")

        #rospy.loginfo(f"{self.ServerName_} Select point got Matix = {matrix_}")
        #rospy.loginfo(f"{self.ServerName_} Select point got num_rows = {num_rows}")
        feedback_msg = ChooseGoalFeedback()
        # Array to pass the goal
        _goal_arr_ = []
        # Reshape the matrix
        matrix = np.array(matrix_).reshape(np.sum(num_rows), 3)

        
        if matrix[:, 0] != []:
            # Point for the goal
            p = Point2D()

            # TODO update the reward if the chosen goal array has already come goals inside
            if chosen_coords != []:
                #rospy.loginfo(f"{self.ServerName_} Updating the reward for the next goals according to the already chosen ones ... ")
                matrix = self.update_rewards(chosen_coords, matrix)
                pass
            
            # Get indices of maximum reward in submatrix
            max_reward_idx = np.argmax(matrix[:, 0])

            # Get coordinates of maximum reward in submatrix
            p.x = round(matrix[max_reward_idx, 1], 2)
            p.y = round(matrix[max_reward_idx, 2], 2)

            # Check if coordinates are already chosen
            for point in chosen_coords:
                if p.x == point.x and p.y == point.y:
                    # If coordinates already chosen, find next maximum
                    matrix[max_reward_idx, 0] = -np.inf
                    max_reward_idx = np.argmax(matrix[:, 0])
                    p.x = round(matrix[max_reward_idx, 1], 2)
                    p.y = round(matrix[max_reward_idx, 2], 2)

            # Store chosen coordinates as an array
            chosen_coords.append(p)
            
            rospy.loginfo(f"{self.ServerName_} chosen_coords after assignment : {chosen_coords}")

            # Array to pass the goal
            _goal_arr_ = [p]

            # Print log
            log_message = f"{self.ServerName_} Points chosen:\n"
            log_message += f"x: {p.x}, y: {p.y}\n"
            rospy.loginfo(log_message)

            # Set the feedback status
            feedback_msg.status = True

        return _goal_arr_
    
    # Function to update the distance of the frontiers
    # The function takes the already chosen coordinates for the goal
    # of the agents processed so far and the matrix of the remaining
    # agents to choose the goal for
    def update_rewards(self, chosen_coords, matrix):
        # Store the max among the rewards
        _max_ = np.max(matrix[:,0])

        # By dividing the maximum reward among the chosen points, you ensure that K is adjusted relative to the magnitude of the rewards.
        # This approach helps maintain a reasonable scaling factor that takes into account the range of rewards in the matrix and the number of chosen points.
        K = _max_ / len(chosen_coords)

        for c in range(len(chosen_coords)):
            for g in range(len(matrix)):
                # Check that the point is not already present in the choosing coordinate.
                # If so then set to -inf
                d1 = pow(chosen_coords[c].x-matrix[g,1],2)+pow(chosen_coords[c].y-matrix[g,2],2)
                if (chosen_coords[c].x == matrix[g,1] and chosen_coords[c].y == matrix[g,2]) or (d1<INTER_GOAL_DIST):
                    #rospy.logwarn(f"Point [{str(matrix[g, 1])},{str(matrix[g, 2])}] already chosen or too close with distance of :{d1} from setvalue of {INTER_GOAL_DIST}. Reward set to -inf")
                    matrix[g,0] = -np.inf
                # Check that the reward is not -inf
                if matrix[g,0] != -np.inf:
                    # Compute the squared distance from the goals already chosen and all the possible other goals
                    d2 = pow(chosen_coords[c].x-matrix[g,1],2)+pow(chosen_coords[c].y-matrix[g,2],2)
                    if d2 != 0.0:
                        # Update the reward with a -k/d^2 coefficient normalized with respect to the max distance
                        matrix[g,0] -= (K/d2)
                    else:
                        matrix[g,0] = -np.inf

        return matrix
    


    def chosen_coords_and_info(self, x, y, text):
        return {'point': (x, y), 'info': text}

def initialize_points(self):
    global chosen_coords_with_info
    chosen_coords_with_info = [
        self.chosen_coords_and_info(1.0, 2.0, 'Point 1'),
        self.chosen_coords_and_info(3.0, 4.0, 'Point 2'),
        self.chosen_coords_and_info(5.0, 6.0, 'Point 3')
    ]



# Define the array of 2D points with text info
points_with_text = [
    {'point': (x, y), 'info': text}
    for x, y, text in [(1.0, 2.0, 'Point 1'), (3.0, 4.0, 'Point 2'), (5.0, 6.0, 'Point 3')]
]


if __name__ == '__main__':
    rospy.init_node('choose_points_server')
    server = ChoosePointsServer('ChoosePointsServer')
    rospy.spin()
