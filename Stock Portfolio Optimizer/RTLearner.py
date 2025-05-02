import numpy as np
import scipy.stats as st

class RTLearner(object):
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    This is a Random Tree Regression Learner.

    """  		  	   		 	   		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1):
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 	   		  		  		    	 		 		   		 		  
        """
        self.tree = None
        self.leaf_size = leaf_size


    def add_evidence(self, data_x, data_y):
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		 	   		  		  		    	 		 		   		 		  

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """

        # build and save the model
        data = np.column_stack((data_x, data_y))
        self.tree = self.build_tree(data)

    def build_tree(self, data):

        l = data.shape[1]
        if data.shape[0] <= self.leaf_size or np.unique(data[:, -1]).size == 1:
            return np.array([[-1, st.mode(data[:, -1])[0] , 0, 0]])
        i = np.random.randint(1, l-1)
        split_arr = data[:, i]
        split_val = np.mean(split_arr)
        left_data = data[data[:, i] <= split_val]
        right_data = data[data[:, i] > split_val]
        if np.unique(split_arr).size == 1 or np.array_equal(left_data, data) or np.array_equal(right_data, data):
            return np.array([[-1, st.mode(data[:, -1])[0] , 0, 0]])
        """if (len(np.unique(data[data[:, i] <= split_val]) == 1)) or (len(np.unique(data[data[:, i] > split_val]) == 1)):
            data = data[data[:, i] <= split_val]
            return np.array([[-1, data[0, - 1], 0, 0]])"""
        left_tree = self.build_tree(left_data)
        right_tree = self.build_tree(right_data)
        root = np.array([[i, split_val, 1, left_tree.shape[0] + 1]])
        tree = np.row_stack((root, left_tree, right_tree))
        return tree

    def best_feature_split(self, data, l):
        correlation_arr = np.zeros(l - 1)
        for x in range(l - 1):
            correlation_arr[x] = abs(np.corrcoef(data[:, x], data[:, l - 1])[0, 1])
        i = np.argmax(correlation_arr)
        return int(i)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        if len(points.shape) == 1:
            pred_y = np.array([0])
        else:
            pred_y = np.zeros(points.shape[0])
        for i in range(len(pred_y)):
            pred_y[i] = self.traverse_tree(self.tree, points, i, 0)
        return pred_y

    def traverse_tree(self, tree, points, i, root):
        """
        Add training data to learner

        :param tree: A set of feature values used to train the learner
        :type tree: numpy.ndarray
        :param points: The value we are attempting to predict given the X data
        :type points: numpy.ndarray
        :param i: The index of the current node in the tree
        :type i: int
        :param root: The current node in the tree
        :type root: int
        """
        if tree[int(root), 0] == -1:
            return tree[int(root), 1]
        if len(points.shape) == 1:
            if points[int(tree[int(root), 0])] <= tree[int(root), 1]:
                return self.traverse_tree(tree, points, i, root + tree[int(root), 2])
            else:
                return self.traverse_tree(tree, points, i, root + int(tree[int(root), 3]))
        else:
            if points[i, int(tree[int(root), 0])] <= tree[int(root), 1]:
                return self.traverse_tree(tree, points, i, root + tree[int(root), 2])
            else:
                return self.traverse_tree(tree, points, i, root + tree[int(root), 3])
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    pass
