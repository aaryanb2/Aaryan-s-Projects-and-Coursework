
import numpy as np
import scipy.stats as st

class BagLearner(object):
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    This is a Bagging Regression Learner.

    """  		  	   		 	   		  		  		    	 		 		   		 		  
    def __init__(self, learner, kwargs = {"argument1":1, "argument2":2}, bags = 20, boost = False, verbose = False):
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 	   		  		  		    	 		 		   		 		  
        """
        self.learners = None
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
  		  	   		 	   		  		  		    	 		 		   		 		  
    def add_evidence(self, data_x, data_y):  		  	   		 	   		  		  		    	 		 		   		 		  
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		 	   		  		  		    	 		 		   		 		  		  	   		 	   		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		 	   		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		 	   		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		 	   		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		 	   		  		  		    	 		 		   		 		  
        """
  		  	   		 	   		  		  		    	 		 		   		 		  
        # build and save the model
        self.learners = []
        for i in range(0, self.bags):
            self.learners.append(self.learner(**self.kwargs))
        for l in self.learners:
            random_bag = np.random.choice(data_x.shape[0], data_x.shape[0], replace=True)
            x_test = data_x[random_bag, :]
            y_test = data_y[random_bag]
            l.add_evidence(x_test, y_test)
        

    def query(self, points):
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		 	   		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		 	   		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		 	   		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		 	   		  		  		    	 		 		   		 		  
        """
        predicted = np.zeros([len(self.learners), points.shape[0]])
        i = 0
        for l in self.learners:
            predicted[i, :] = l.query(points)
            i += 1
        a = st.mode(predicted)[0]
        return a
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    pass

