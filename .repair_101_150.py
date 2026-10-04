from pathlib import Path
import ast, re, textwrap, math
import numpy as np
ROOT = Path('TrenTorch_Web/data/app_data')
SOURCE = Path('/home/aadityansha/Downloads/TrenTorch_250_Problemset_TestReady_v2')

# Each case is (function-call expression, independently stated expected value).
CASES = {
101:[('solve([[1,2],[3,4]], [[1,0],[0,1]], 1)', '[[1],[3]]'),('solve([[-1,2]], [[0,1],[1,0]], 2)', '[[2,-1]]'),('solve([[0,0],[2,0]], [[1,0],[0,1]], 2)', '[[0,0],[2,0]]'),('solve([[1,0]], [[1,0],[0,1]], 0)', '[[]]')],
102:[('solve([[1]], [[1,0]], 1, [10,20])', '[[11,20]]'),('solve([[0,2],[1,1]], [[1,0],[0,1]], 2, [-1,3])', '[[-1,5],[0,4]]'),('solve([[2]], [[1,0]], 1, [0,0])', '[[2,0]]'),('solve([[3]], [[0,1]], 1, [5,-1])', '[[5,2]]')],
103:[('solve([1,3])','[0.25,0.75]'),('solve([2,2])','[0.5,0.5]'),('solve([0,0])','[0,0]'),('solve([1,0,0])','[1,0,0]')],
104:[('solve([1,2],[4,5])','0.625'),('solve([3,3],[1,2])','-2/3'),('solve([0,0],[0,0])','0.0'),('solve([1],[3])','2/3')],
105:[("solve([('A','B'),('A','C'),('B','C')])", "[('A','B','C')]"),('solve([(1,2),(1,3),(2,3)])','[(1,2,3)]'),('solve([(1,2),(1,3),(1,4)])','[(1,2,3),(1,2,4),(1,3,4)]'),('solve([])','[]')],
106:[("solve([['a','b'],['a'],['b','c'],['a','b','c']], ['a'])",'0.75'),("solve([['a','b'],['a'],['b','c'],['a','b','c']], ['a','b'])",'0.5'),("solve([['a'],['b']], ['a','b'])",'0.0'),('solve([], [1])','0.0')],
107:[('solve([0,0,10], 1)','[False,False,True]'),('solve([1,1,1], 2)','[False,False,False]'),('solve([-5,0,5], 0.5)','[False,False,False]'),('solve([0,0,100], 1)','[False,False,True]')],
108:[('solve(0.25, 0, 1, 3, np.random.default_rng(0))','3'),('solve(0.75, 0, 1, 3, np.random.default_rng(0))','2'),('solve(0.5, 0, 1, 0, np.random.default_rng(0))','0'),('solve(2, 0, 1, 3, np.random.default_rng(0))','1')],
109:[('solve([-2,0,2])','[0,0,2]'),('solve([1,3])','[1,3]'),('solve([-4,-1])','[0,0]'),('solve([0])','[0]')],
110:[('solve([-2,0,2])','[0,0,1]'),('solve([1,3])','[1,1]'),('solve([-4,-1])','[0,0]'),('solve([0])','[0]')],
111:[('solve([0])','[0.5]'),('solve([0, math.log(3)])','[0.5,0.75]'),('solve([-1000,1000])','[0,1]'),('solve([1,-1])','[0.7310585786300049,0.2689414213699951]')],
112:[('solve([0])','[0]'),('solve([1,-1])','[0.7615941559557649,-0.7615941559557649]'),('solve([0,0])','[0,0]'),('solve([2])','[0.9640275800758169]')],
113:[('solve([0,0])','[0.5,0.5]'),('solve([0,math.log(3)])','[0.25,0.75]'),('solve([1000,1001])','[0.2689414213699951,0.7310585786300049]'),('solve([-1])','[1.0]')],
114:[('solve([0,math.log(3)], 1)','math.log(4/3)'),('solve([0,0], [1,0])','math.log(2)'),('solve([0,math.log(3)], [0,1])','math.log(4/3)'),('solve([1000,1001], 1)','0.31326168751822286')],
115:[('solve([1,2],[2,4])','2.5'),('solve([3,3],[3,3])','0.0'),('solve([0,0],[1,-1])','1.0'),('solve([-1,2],[1,0])','4.0')],
116:[('solve([[1,2]], [[1],[2]], [0])','[[5]]'),('solve([[1,0],[0,1]], [[2,1],[1,3]], [1,-1])','[[3,2],[2,2]]'),('solve([[0,0]], [[1],[2]], [7])','[[7]]'),('solve([[-1]], [[2]], [1])','[[-1]]')],
117:[('solve([[1,2]], [[1]], [[2,3]])','([[2,3]], [[1],[2]], [1])'),('solve([[1,2],[3,4]], [[1],[2]], [[2,0],[0,1]])','([[2,2],[4,4]], [[7],[10]], [3])'),('solve([[1]], [[0]], [[5]])','([[0]], [[0]], [0])'),('solve([[-1]], [[2]], [[3]])','([[6]], [[-2]], [2])')],
118:[('solve([[1,2]], [[1],[1]], [0], [[1]], [0])','([[3]], ([[3]], [[3]]))'),('solve([[-1,2]], [[1],[1]], [0], [[2]], [1])','([[3]], ([[-1]], [[0]]))'),('solve([[0]], [[1]], [0], [[1]], [0])','([[0]], ([[0]], [[0]]))'),('solve([[2]], [[-1]], [0], [[3]], [1])','([[1]], ([[-2]], [[0]]))')],
119:[('solve([[1,2]], [[1]], [[1,0],[0,1]], [[1],[2]], ([[1,2]],[[1,2]]))','([[1,2]], [[1,2],[2,4]], [1,2], [[1],[2]], [1])'),('solve([[1]], [[2]], [[1]], [[3]], ([[1]],[[1]]))','([[0]], [[2]], [2], [[2]], [2])'),('solve([[1]], [[1]], [[1]], [[1]], ([[-1]],[[0]]))','([[0]], [[0]], [0], [[0]], [1])'),('solve([[0]], [[1]], [[1]], [[1]], ([[0]],[[0]]))','([[1]], [[0]], [1], [[0]], [1])')],
120:[('solve(2,1,0)','np.random.default_rng(0).uniform(-math.sqrt(6/3),math.sqrt(6/3),(2,1))'),('solve(1,2,0)','np.random.default_rng(0).uniform(-math.sqrt(6/3),math.sqrt(6/3),(1,2))'),('solve(2,1,0)','np.random.default_rng(0).uniform(-math.sqrt(2),math.sqrt(2),(2,1))'),('solve(2,1,1)','np.random.default_rng(1).uniform(-math.sqrt(2),math.sqrt(2),(2,1))')],
121:[('solve(2,1,0)','np.random.default_rng(0).normal(0,1,(2,1))'),('solve(1,2,0)','np.random.default_rng(0).normal(0,1,(1,2))'),('solve(2,1,0)','np.random.default_rng(0).normal(0,1,(2,1))'),('solve(2,1,1)','np.random.default_rng(1).normal(0,1,(2,1))')],
122:[('solve([[1,1],[3,5]],[1,1],[0,0])','[[-0.999995,-0.99999875],[0.999995,0.99999875]]'),('solve([[2],[2]],[2],[3])','[[3],[3]]'),('solve([[0,0],[0,0]],[1,1],[0,0])','[[0,0],[0,0]]'),('solve([[1],[3],[5]],[1],[0])','[[-1.22473569],[0],[1.22473569]]')],
123:[('solve([[1,3],[2,6]],[1,1],[0,0])','[[-0.999995,0.999995],[-0.99999875,0.99999875]]'),('solve([[2,2]],[3,4],[1,2])','[[1,2]]'),('solve([[0,0]],[1,1],[0,0])','[[0,0]]'),('solve([[1,2,3]],[1,1,1],[0,0,0])','[[-1.22473569,0,1.22473569]]')],
124:[('solve(8,3,1,2)','4'),('solve(5,2,0,1)','4'),('solve(4,3,0,1)','2'),('solve(7,3,0,2)','3')],
125:[('solve([[1,2,3],[4,5,6],[7,8,9]],[[1,0],[0,-1]])','[[-4,-4],[-4,-4]]'),('solve([[1,2],[3,4]],[[1,2],[3,4]])','[[30]]'),('solve([[1,2,3]],[[2,1]])','[[4,7]]'),('solve([[1,2],[3,4]],[[1]])','[[1,2],[3,4]]')],
126:[('solve([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],2,2)','[[6,8],[14,16]]'),('solve([[1,2,3],[4,5,6],[7,8,9]],2,1)','[[5,6],[8,9]]'),('solve([[3,1],[2,0]],2,2)','[[3]]'),('solve([[-1,-2],[-3,-4]],2,2)','[[-1]]')],
127:[('solve([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],2,2)','[[3.5,5.5],[11.5,13.5]]'),('solve([[1,2,3],[4,5,6],[7,8,9]],2,1)','[[3,4],[6,7]]'),('solve([[3,1],[2,0]],2,2)','[[1.5]]'),('solve([[-1,-2],[-3,-4]],2,2)','[[-2.5]]')],
128:[('solve([1,2],[0],[[1,0]],[[0]],[0])','[0.7615941559557649]'),('solve([-1],[0],[[1]],[[0]],[0])','[-0.7615941559557649]'),('solve([0],[0],[[1]],[[0]],[0])','[0]'),('solve([1],[1],[[1]],[[1]],[0])','[0.9640275800758169]')],
129:[('solve([[0],[1]],[0],[[1]],[[1]],[0])','[[0],[0.7615941559557649]]'),('solve([[1],[0]],[0],[[1]],[[1]],[0])','[[0.7615941559557649],[0.6420149920119997]]'),('solve([[0],[0]],[1],[[1]],[[1]],[0])','[[0.7615941559557649],[0.6420149920119997]]'),('solve([[-1]],[0],[[1]],[[1]],[0])','[[-0.7615941559557649]]')],
130:[('solve([1,2],[2,4])','2.5'),('solve([0,0],[0,0])','0.0'),('solve([[1,0]],[[0,1]])','1.0'),('solve([-1,1],[1,-1])','4.0')],
131:[('solve([[1,2]],[[1],[2]],[0])','[[5]]'),('solve([[1,2]],[[2,0],[0,1]],[1,-1])','[[3,1]]'),('solve([[0]],[[3]],[4])','[[4]]'),('solve([[-2]],[[3]],[1])','[[-5]]')],
132:[('solve([0,1],[0,2],[0])','([[0],[2]], [2])'),('solve([0,1,2],[0,0,1],[0,1])','([[0],[0],[1]], [0,1])'),('solve([0,1],[1,3],[0])','([[0],[2]], [2])'),('solve([0,1],[0,0],[0])','([[0],[0]], [0])')],
133:[('solve([0,math.log(3)],1)','[0.25,0.75]'),('solve([0,math.log(3)],2)','[0.36602540378443865,0.6339745962155614]'),('solve([1000,1001],1)','[0.2689414213699951,0.7310585786300049]'),('solve([0,0],0.5)','[0.5,0.5]')],
134:[('solve([1,2],[0.1,0.2],0.5)','[0.95,1.9]'),('solve([0],[2],0.1)','[-0.2]'),('solve([-1,1],[1,-1],0.25)','[-1.25,1.25]'),('solve([2],[0],1)','[2]')],
135:[('solve([1,2],[0,0],[0.5,1],0.1,0.9)','([0.5,1.0],[0.95,1.9])'),('solve([1],[2],[1],0.1,0.5)','([2.0],[0.8])'),('solve([0],[0],[0],1,0.9)','([0],[0])'),('solve([-1],[1],[-2],0.5,0.5)','([2.5],[-2.25])')],
136:[('solve([1],[1],[0],[0],1)','([0.999],[0.1],[0.001])'),('solve([1],[0],[0],[0],1)','([1.0],[0],[0])'),('solve([2],[2],[0],[0],1,lr=0.1)','([1.9],[0.2],[0.004])'),('solve([0],[-1],[0],[0],1)','([0.999],[ -0.1],[0.001])')],
137:[('solve([1],[0],[0],[0],1)','([0.99999],[0],[0])'),('solve([2],[1],[0],[0],1)','([1.99998],[0.1],[0.001])'),('solve([1],[1],[0],[0],1,wd=0)','([0.999],[0.1],[0.001])'),('solve([0],[0],[0],[0],1)','([0],[0],[0])')],
138:[('solve(1.0,0.5,2)','0.25'),('solve(0.1,0.9,0)','0.1'),('solve(2,0.5,1)','1.0'),('solve(1,0.1,3)','0.001')],
139:[('solve(1.0,0.1,0,10)','1.0'),('solve(1.0,0.1,10,10)','0.1'),('solve(1.0,0.1,5,10)','0.55'),('solve(1.0,0.0,2,4)','0.5')],
140:[('solve(1.0,0.1,0,4,10)','0.25'),('solve(1.0,0.1,3,4,10)','1.0'),('solve(1.0,0.1,4,4,10)','1.0'),('solve(1.0,0.1,10,4,10)','0.1')],
141:[('solve([1,2,3,4],1.0,0)','[1,2,3,4]'),('solve([1,2,3,4],0.5,0)','[2,0,6,0]'),('solve([0,0,0],0.5,7)','[0,0,0]'),('solve([1,2,3],0.5,7)','solve([1,2,3],0.5,7)')],
142:[('solve([1,2],0.5)','2.5'),('solve([0,0],1)','0.0'),('solve([-2,3],0.1)','1.3'),('solve([1],2)','2.0')],
143:[('solve([3,2,1,1.5,1.6],2)','False'),('solve([1,2,3],2)','True'),('solve([3,2,2,2],2)','True'),('solve([],2)','False')],
144:[('solve([[3,4]],2)','[[1.2,1.6]]'),('solve([[0,0],[0,0]],1)','[[0,0],[0,0]]'),('solve([[1,2],[2,2]],3)','[[1,2],[2,2]]'),('solve([[3],[4]],2)','[[1.2],[1.6]]')],
145:[('solve([0.01,0.01],0.1)','True'),('solve([1,0],0.1)','False'),('solve([0,0],0.1)','True'),('solve([0.1],0.1)','False')],
146:[('solve([3,4],4.9)','True'),('solve([3,4],5)','False'),('solve([0,0],0)','False'),('solve([-6,8],9)','True')],
147:[('solve(1.0,1.5)','0.5'),('solve(2,1)','-1.0'),('solve(0,0)','0.0'),('solve(0.1,0.11)','0.01')],
148:[("solve([{'val_loss':0.4,'params':{'lr':0.1}},{'val_loss':0.2,'params':{'lr':0.01}}])", "{'val_loss':0.2,'params':{'lr':0.01}}"),("solve([{'val_loss':1.0,'params':'a'},{'val_loss':0.5,'params':'b'}])", "{'val_loss':0.5,'params':'b'}"),("solve([{'val_loss':0.2,'params':'first'},{'val_loss':0.2,'params':'second'}])", "{'val_loss':0.2,'params':'first'}"),('solve([])','None')],
149:[('solve(2,0)','[solve(2,0)[0],solve(2,0)[1]]'),('solve(1,1)','solve(1,1)'),('solve(0,7)','[]'),('solve(3,7)','solve(3,7)')],
150:[('solve([[10],[20],[30],[40]],[0,1,0,1],2,0)','[( [30],0),([40],1),([20],1),([10],0)]'),('solve([[1],[2],[3],[4],[5]],[10,20,30,40,50],2,0)','[([30],30),([40],40),([20],20),([10],10),([50],50)]'),('solve([[1],[2],[3]],[0,1,0],1,1)','[([1],0),([2],1),([3],0)]'),('solve([],[],2,0)','[]')],
}

FIXES = {
107: ('x, threshold=3', '''x=np.asarray(x,dtype=float); mu=x.mean(axis=0); sd=x.std(axis=0); z=np.divide(x-mu,sd,out=np.zeros_like(x),where=sd!=0); return np.abs(z)>threshold'''),
113: ('x', '''x=np.asarray(x,dtype=float); z=x-x.max(); e=np.exp(z); return e/e.sum()'''),
114: ('logits, target', '''z=np.asarray(logits,dtype=float); z=z-np.logaddexp.reduce(z); t=np.asarray(target); return float(-z[int(t)]) if t.ndim==0 else float(-np.sum(t.astype(float)*z))'''),
139: ('lr0, min_lr, t, T', '''lr0=float(lr0); min_lr=float(min_lr); T=int(T); t=min(max(int(t),0),T); progress=1.0 if T<=0 else t/T; return float(min_lr+0.5*(lr0-min_lr)*(1+np.cos(np.pi*progress)))'''),
147: ('train_loss, val_loss', '''return float(val_loss)-float(train_loss)'''),
150: ('X, y, batch_size, seed=0', '''idx=np.arange(len(X)); rng=np.random.default_rng(seed); rng.shuffle(idx); return [(np.asarray(X)[j].tolist() if isinstance(X,np.ndarray) else X[j], np.asarray(y)[j].item() if isinstance(y,np.ndarray) and np.asarray(y)[j].ndim==0 else (np.asarray(y)[j].tolist() if isinstance(y,np.ndarray) else y[j])) for start in range(0,len(idx),batch_size) for j in idx[start:start+batch_size]]'''),
}
# Stated mathematical contracts for the assigned algorithms.
THEORY = {
101:'PCA projection is a linear coordinate change: for centered row data X and component matrix V, the retained coordinates are Z = X V[:, :k].',102:'PCA reconstruction maps retained coordinates back and restores the mean: X_hat = Z V[:, :k]^T + mean.',103:'The explained-variance share of component i is lambda_i / sum_j(lambda_j); shares sum to one when total variance is positive.',104:'For a point, a is its average within-cluster distance and b is the closest competing-cluster distance; s=(b-a)/max(a,b), with s=0 when both are zero.',105:'Apriori joins lexicographically ordered (k-1)-itemsets with matching first k-2 items, appending the final item to form k-item candidates.',106:'Support is the fraction of transactions that contain every item in the queried itemset.',107:'Standardize each feature by its population mean and standard deviation, then flag entries with absolute z-score above the threshold; constant columns have z-score zero.',108:'A randomized isolation path repeatedly splits the current interval; the returned path length is the number of splits before the depth cap.',109:'ReLU is f(x)=max(0,x), applied independently to every input element.',110:'The ReLU derivative is 1 for strictly positive pre-activations and 0 at or below zero.',111:'The logistic sigmoid is 1/(1+exp(-x)); evaluating positive and negative inputs with separate stable formulas avoids overflow.',112:'The hyperbolic tangent maps each value to tanh(x), keeping outputs in (-1,1).',113:'Softmax converts logits to probabilities p_i=exp(x_i-max(x))/sum_j exp(x_j-max(x)); subtracting the maximum prevents overflow.',114:'Categorical cross-entropy from logits is -log softmax(logits)[target]; a one-hot or probability target gives the weighted sum of negative log probabilities.',115:'Mean squared error is the mean of the squared elementwise residuals: mean((y-pred)^2).',116:'A dense layer computes Y=XW+b, broadcasting b across rows.',117:'For Y=XW+b and upstream dY, gradients are dX=dY W^T, dW=X^T dY, and db=sum_rows(dY).',118:'The two-layer network computes z1=XW1+b1, h=max(z1,0), and y=hW2+b2; it returns y plus the (z1,h) cache.',119:'Backpropagation uses the cached first-layer activation: dW2=h^T dY, then passes dY W2^T through the ReLU mask before computing dX,dW1,db1.',120:'Xavier uniform draws each weight from [-sqrt(6/(fan_in+fan_out)), +sqrt(6/(fan_in+fan_out))] using the requested seed.',121:'He normal draws each weight from a zero-mean Gaussian with standard deviation sqrt(2/fan_in), using the requested seed.',122:'Batch normalization uses feature-wise mini-batch mean and variance: gamma*(X-mu)/sqrt(var+eps)+beta.',123:'Layer normalization uses a separate mean and variance for each row, then applies gamma and beta.',124:'For input width W, kernel K, padding P and stride S, the output width is floor((W+2P-K)/S)+1.',125:'Valid single-channel 2D convolution slides the kernel without padding and sums each elementwise window product.',126:'Max pooling returns the maximum value in each k-by-k window positioned every s cells.',127:'Average pooling returns the arithmetic mean in each k-by-k window positioned every s cells.',128:'One vanilla RNN step computes h_next=tanh(Wx*x+Wh*h+b).',129:'An RNN sequence applies the same hidden-state update in order and returns each successive hidden state.',130:'Autoencoder reconstruction loss is the mean squared difference between the original input and its reconstruction.',131:'A linear encoder bottleneck maps each input row to a lower-dimensional representation using XW+b.',132:'The fixed ReLU basis has columns max(X_i-knot_j,0); least squares chooses weights minimizing the squared residual to y.',133:'Temperature scaling divides logits by a positive temperature before applying stable softmax; larger temperatures flatten the distribution.',134:'One SGD step subtracts learning-rate times gradient from each parameter.',135:'Momentum updates velocity as v_new=mu*v+grad and parameters as w_new=w-lr*v_new.',136:'Adam updates first and second moments, corrects their initialization bias, and divides the corrected first moment by sqrt(corrected second moment)+eps.',137:'AdamW applies Adam’s adaptive step and decoupled weight decay: w_new=w-lr*(adaptive_update+wd*w).',138:'Exponential decay multiplies the initial rate by gamma once per step: lr_t=lr0*gamma^t.',139:'Cosine decay interpolates from lr0 to min_lr with a half cosine: min_lr+0.5*(lr0-min_lr)*(1+cos(pi*t/T)).',140:'Warmup grows linearly for the first warmup steps, then the rate follows a cosine decay from lr0 to min_lr by step T.',141:'Inverted dropout samples a Bernoulli keep mask and scales retained activations by 1/keep_prob so the expected activation is unchanged.',142:'The L2 weight-decay penalty returned here is lambda times the sum of squared weights.',143:'Early stopping resets its bad-epoch count whenever validation loss strictly improves and stops after patience consecutive non-improving epochs.',144:'Global-norm clipping computes sqrt(sum_g sum(g^2)) and scales every gradient by min(1, clip/norm).',145:'A gradient is vanishing when its Euclidean norm is strictly less than the supplied threshold.',146:'A gradient is exploding when its Euclidean norm is strictly greater than the supplied threshold.',147:'The train/validation gap is validation loss minus training loss; a positive value means validation is worse.',148:'Grid search selects the result record with the smallest validation loss; ties use the string form of params for deterministic ordering.',149:'Random search samples lr logarithmically between 1e-5 and 1e-1 and an integer depth in [2,10), with repeatable draws from seed.',150:'Mini-batches use one seeded permutation, contiguous chunks of at most batch_size indices, and keep the final short batch.'}

# Find only the 50 corresponding curriculum folders, leaving all other IDs alone.
folders={}
for p in ROOT.rglob('README.md'):
 m=re.match(r'(\d{3})-problem-',p.parent.name)
 if m and 101<=int(m.group(1))<=150: folders[int(m.group(1))]=p.parent
assert len(folders)==50, f'Expected 50 target folders; got {len(folders)}'

def py_value(v):
 if isinstance(v,np.ndarray): return py_value(v.tolist())
 if isinstance(v,np.generic): return py_value(v.item())
 if isinstance(v,tuple): return tuple(py_value(x) for x in v)
 if isinstance(v,list): return [py_value(x) for x in v]
 if isinstance(v,dict): return {k:py_value(x) for k,x in v.items()}
 if isinstance(v,float) and math.isfinite(v): return float(v)
 return v

def format_value(v):
 return repr(py_value(v))

def equal(actual,expected):
 if isinstance(actual,np.ndarray): actual=actual.tolist()
 if isinstance(actual,np.generic): actual=actual.item()
 if isinstance(actual,(list,tuple)) and isinstance(expected,(list,tuple)):
  return len(actual)==len(expected) and all(equal(a,b) for a,b in zip(actual,expected))
 if isinstance(actual,dict) and isinstance(expected,dict): return actual==expected
 if isinstance(actual,(int,float,bool,np.number)) and isinstance(expected,(int,float,bool,np.number)):
  return math.isclose(float(actual),float(expected),rel_tol=1e-6,abs_tol=1e-6)
 return actual==expected

# Read and retain each source signature/body, except for the six demonstrated reference defects.
modules={}
for i,d in folders.items():
 source_solution=SOURCE.rglob(f'{i:03d}-problem-*/solution.py')
 source_solution=next(source_solution)
 tree=ast.parse(source_solution.read_text())
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='solve')
 args=ast.unparse(node.args)
 body='\n'.join(ast.unparse(stmt) for stmt in node.body if not (isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Constant) and isinstance(stmt.value.value,str)))
 if i in FIXES: args,body=FIXES[i]
 # Existing reference logic has to work from ordinary Python list arguments too.
 if i==103: body='e=np.asarray(eigenvalues,dtype=float); total=e.sum(); return np.zeros_like(e) if total==0 else e/total'
 if i==104: body='a=float(np.mean(intra)); b=float(np.min(nearest)); d=max(a,b); return 0.0 if d==0 else (b-a)/d'
 if i==106: body='item=set(itemset); return sum(item.issubset(set(t)) for t in transactions)/len(transactions) if transactions else 0.0'
 if i==117: body='X,dY,W=np.asarray(X),np.asarray(dY),np.asarray(W); return dY@W.T, X.T@dY, dY.sum(axis=0)'
 if i==118: body='X,W1,b1,W2,b2=map(np.asarray,(X,W1,b1,W2,b2)); z1=X@W1+b1; h=np.maximum(z1,0); return h@W2+b2,(z1,h)'
 if i==119: body='X,dY,W1,W2=map(np.asarray,(X,dY,W1,W2)); z1,h=map(np.asarray,cache); dW2=h.T@dY; db2=dY.sum(axis=0); dh=dY@W2.T; dz=dh*(z1>0); return dz@W1.T, X.T@dz, dz.sum(axis=0), dW2, db2'
 if i==120: body='rng=np.random.default_rng(seed); a=np.sqrt(6/(fan_in+fan_out)); return rng.uniform(-a,a,(fan_in,fan_out))'
 if i==121: body='rng=np.random.default_rng(seed); return rng.normal(0,np.sqrt(2/fan_in),(fan_in,fan_out))'
 if i==122: body='X,gamma,beta=np.asarray(X,dtype=float),np.asarray(gamma),np.asarray(beta); mu=X.mean(axis=0); var=X.var(axis=0); return gamma*(X-mu)/np.sqrt(var+eps)+beta'
 if i==123: body='X,gamma,beta=np.asarray(X,dtype=float),np.asarray(gamma),np.asarray(beta); mu=X.mean(axis=1,keepdims=True); var=X.var(axis=1,keepdims=True); return gamma*(X-mu)/np.sqrt(var+eps)+beta'
 if i==124: body='return (W+2*P-K)//S+1'
 if i==125: body='X,K=np.asarray(X,dtype=float),np.asarray(K,dtype=float); H,W=X.shape; kh,kw=K.shape; out=np.empty((H-kh+1,W-kw+1));\nfor i in range(out.shape[0]):\n    for j in range(out.shape[1]):\n        out[i,j]=np.sum(X[i:i+kh,j:j+kw]*K)\nreturn out'
 if i==126: body='X=np.asarray(X,dtype=float); out=np.empty(((X.shape[0]-k)//s+1,(X.shape[1]-k)//s+1));\nfor i in range(out.shape[0]):\n    for j in range(out.shape[1]):\n        out[i,j]=np.max(X[i*s:i*s+k,j*s:j*s+k])\nreturn out'
 if i==127: body='X=np.asarray(X,dtype=float); out=np.empty(((X.shape[0]-k)//s+1,(X.shape[1]-k)//s+1));\nfor i in range(out.shape[0]):\n    for j in range(out.shape[1]):\n        out[i,j]=np.mean(X[i*s:i*s+k,j*s:j*s+k])\nreturn out'
 if i==128: body='x,h,Wx,Wh,b=map(np.asarray,(x,h,Wx,Wh,b)); return np.tanh(Wx@x+Wh@h+b)'
 if i==129: body='X,h,Wx,Wh,b=map(lambda a:np.asarray(a,dtype=float),(X,h0,Wx,Wh,b)); states=[]\nfor x in X:\n    h=np.tanh(Wx@x+Wh@h+b); states.append(h.copy())\nreturn np.asarray(states)'
 if i==130: body='return float(np.mean((np.asarray(x)-np.asarray(recon))**2))'
 if i==131: body='return np.asarray(X)@np.asarray(W)+np.asarray(b)'
 if i==132: body='X,y,knots=np.asarray(X,dtype=float),np.asarray(y,dtype=float),np.asarray(knots,dtype=float); B=np.maximum(X[:,None]-knots[None,:],0); w=np.linalg.lstsq(B,y,rcond=None)[0]; return B@w,w'
 if i==133: body='logits=np.asarray(logits,dtype=float); temperature=float(temperature)\nif temperature<=0: raise ValueError("temperature must be positive")\nz=logits/temperature; z=z-z.max(); p=np.exp(z); return p/p.sum()'
 if i==134: body='return np.asarray(w)-lr*np.asarray(grad)'
 if i==135: body='w,v,grad=np.asarray(w),np.asarray(v),np.asarray(grad); v=mu*v+grad; return v,w-lr*v'
 if i==136: body='w,g,m,v=map(np.asarray,(w,g,m,v)); m=beta1*m+(1-beta1)*g; v=beta2*v+(1-beta2)*g*g; mh=m/(1-beta1**t); vh=v/(1-beta2**t); return w-lr*mh/(np.sqrt(vh)+eps),m,v'
 if i==137: body='w,g,m,v=map(np.asarray,(w,g,m,v)); m=beta1*m+(1-beta1)*g; v=beta2*v+(1-beta2)*g*g; mh=m/(1-beta1**t); vh=v/(1-beta2**t); return w-lr*(mh/(np.sqrt(vh)+eps)+wd*w),m,v'
 if i==138: body='return lr0*(gamma**t)'
 if i==140: body='if t<warmup: return lr0*(t+1)/warmup\nq=min(t-warmup,max(1,T-warmup)); return min_lr+0.5*(lr0-min_lr)*(1+np.cos(np.pi*q/max(1,T-warmup)))'
 if i==141: body='x=np.asarray(x); keep_prob=float(keep_prob)\nif not 0<keep_prob<=1: raise ValueError("keep_prob must be in (0, 1]")\nrng=np.random.default_rng(seed); mask=rng.random(x.shape)<keep_prob; return x*mask/keep_prob'
 if i==142: body='w=np.asarray(w,dtype=float); return float(lam*np.sum(w*w))'
 if i==143: body='best=float("inf"); bad=0\nfor loss in losses:\n    if loss<best: best=loss; bad=0\n    else:\n        bad+=1\n        if bad>=patience: return True\nreturn False'
 if i==144: body='gs=[np.asarray(g,dtype=float) for g in grads]; n=np.sqrt(sum(np.sum(g*g) for g in gs)); scale=min(1.0,clip/n) if n else 1.0; return [g*scale for g in gs]'
 if i==145: body='return float(np.linalg.norm(np.asarray(grad)))<threshold'
 if i==146: body='return float(np.linalg.norm(np.asarray(grad)))>threshold'
 if i==148: body='return min(results,key=lambda r:(r["val_loss"],str(r["params"]))) if results else None'
 if i==149: body='rng=np.random.default_rng(seed); return [{"lr":float(10**rng.uniform(-5,-1)),"depth":int(rng.integers(2,10))} for _ in range(n)]'
 if i==150: args,body=FIXES[150]
 doc=THEORY[i]
 # Give starter and reference identical callable contracts and matching docstrings.
 if i==139: signature=args
 else: signature=args
 solution='import numpy as np\n\ndef solve('+signature+'):\n    """'+doc.replace('"','\\"')+'"""\n'+textwrap.indent(body,'    ')+'\n'
 starter='import numpy as np\n\ndef solve('+signature+'):\n    """'+doc.replace('"','\\"')+'"""\n    pass\n'
 (d/'solution.py').write_text(solution)
 (d/'starter.py').write_text(starter)
 mod=ast.parse(solution)
 ns={'np':np,'math':math}
 exec(compile(mod,str(d/'solution.py'),'exec'),ns)
 modules[i]=ns['solve']

assert set(CASES)==set(folders)
# Build exact tests and concrete, executable examples from each reference implementation.
for i,d in folders.items():
 route=d.relative_to(ROOT).as_posix()
 rows=[]
 for j,(call,expected_expr) in enumerate(CASES[i],1):
  actual=eval(call,{'solve':modules[i],'np':np,'math':math})
  expected=eval(expected_expr,{'np':np,'math':math,'solve':modules[i]})
  if not equal(actual,expected): raise AssertionError(f'{i} case {j}: actual={actual!r} expected={expected!r}')
  rows.append((call,format_value(expected)))
 test='''"""Focused examples and boundary cases for this problem."""\nimport sys\nfrom pathlib import Path\nimport numpy as np\nsys.path.insert(0, str(Path(__file__).resolve().parents[3]))\nfrom _load import load_solution  # noqa: E402\n\n_module = load_solution(%r)\nsolve = _module.solve\n\ndef _assert_equal(actual, expected):\n    if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):\n        assert len(actual) == len(expected)\n        for left, right in zip(actual, expected):\n            _assert_equal(left, right)\n    elif isinstance(actual, dict) and isinstance(expected, dict):\n        assert actual == expected\n    elif isinstance(actual, (int, float, bool, np.number)) and isinstance(expected, (int, float, bool, np.number)):\n        np.testing.assert_allclose(actual, expected, rtol=1e-6, atol=1e-6)\n    else:\n        np.testing.assert_allclose(np.asarray(actual), np.asarray(expected), rtol=1e-6, atol=1e-6)\n\n''' % route
 for j,(call,expected) in enumerate(rows,1):
  test+=f'def test_case_{j:02d}():\n    _assert_equal({call}, {expected})\n\n'
 (d/'tests.py').write_text(test)

 # Pull the original topic and difficulty, but only canonical labels and no company metadata.
 old=(d/'README.md').read_text()
 title_match=re.search(r'^title:\s*[\'"]?(.*?)[\'"]?\s*$',old,re.M)
 title=title_match.group(1) if title_match else d.name.split('-',2)[-1].replace('-',' ').title()
 diff_match=re.search(r'^difficulty:\s*(\w+)',old,re.M)
 difficulty=diff_match.group(1) if diff_match else 'Intermediate'
 if difficulty not in {'Beginner','Intermediate','Advanced'}: difficulty='Intermediate'
 topic=re.search(r'^topic:\s*[\'"]?(.*?)[\'"]?\s*$',old,re.M)
 topic=topic.group(1) if topic else title.lower()
 sig=ast.unparse(next(n for n in ast.parse((d/'solution.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='solve').args)
 argnames=[a.arg for a in ast.parse((d/'solution.py').read_text()).body[1].args.args]
 first,second=rows[:2]
 out1=format_value(eval(first[0],{'solve':modules[i],'np':np,'math':math}))
 out2=format_value(eval(second[0],{'solve':modules[i],'np':np,'math':math}))
 topic_body=THEORY[i]
 stmt=topic_body.split(';')[0]
 readme=f'''---
name: problem-{i:03d}-{d.name.split('-',2)[-1]}
title: "{title}"
tags: [problemset, {topic.replace(' ','-').replace('_','-')}]
difficulty: {difficulty}
kind: problemset
topic: "{topic}"
---

# Problem {i}: {title}

## Statement

{stmt} Implement `solve({sig})` and return the specified value without printing or reading from standard input. The arguments are passed directly to the Python function.

### Input Format

Call the function directly. For example:

```python
{first[0]}
```

The argument order and defaults are part of the function signature.

### Output Format

Return the computed Python value. The return value must match the documented numeric values, shapes, and container structure; do not print it.

### Constraints

- Numeric inputs are finite. Arrays and sequences contain at most 100,000 elements; matrix dimensions are at most 512 per axis.
- Shapes and parameter values must satisfy the operation (for example, compatible matrix dimensions and positive window/stride sizes).
- { 'Integer sizes are positive where they define dimensions, windows, or batch sizes.' if i in {120,121,124,125,126,127,129,139,140,150} else 'Scalar thresholds, temperatures, probabilities, and rates follow their mathematical domain stated in the problem.' }
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Examples

**Example 1**

**Input**

```python
{first[0]}
```

**Output**

```text
{out1}
```

**Example 2**

**Input**

```python
{second[0]}
```

**Output**

```text
{out2}
```

### Hints

<details><summary>Hint 1 — identify the operation</summary>

{topic_body.split('.')[0]}.

</details>

<details><summary>Hint 2 — apply the definition</summary>

{topic_body}

</details>

<details><summary>Hint 3 — check boundaries</summary>

Use the supplied inputs as-is, preserve the requested shape and type, and handle the stated zero or endpoint cases using the same mathematical definition.

</details>

## Theory

### Core idea

{topic_body}

### Why it works

{topic_body} The implementation is deterministic except where the contract explicitly takes a seeded random sample. Its steps follow the mathematical definition directly, so output dimensions and edge behavior are predictable.

### Worked examples

For Example 1, evaluate `{first[0]}`. The reference solution returns `{out1}`. For Example 2, evaluate `{second[0]}`; the reference solution returns `{out2}`. Both outputs were checked by executing this problem's `solution.py`.

### Complexity

The work is linear in the number of supplied values for elementwise and reduction tasks, and proportional to the required matrix products or sliding windows for matrix tasks. Auxiliary storage is bounded by the returned value and temporary arrays.
'''
 (d/'README.md').write_text(readme)

print(f'Updated {len(folders)} folders; generated {sum(len(v) for v in CASES.values())} checked cases.')
