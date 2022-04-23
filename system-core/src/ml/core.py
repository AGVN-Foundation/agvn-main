# sklearn core
from sklearn.gaussian_process.kernels import ConstantKernel, RBF

kernel = ConstantKernel(constant_value=1.0, constant_value_bounds=(0.0, 10.0)) * RBF(length_scale=0.5,length_scale_bounds=(0.0, 10.0)) + RBF(length_scale=2.0, length_scale_bounds=(0.0, 10.0))

for hyperparameter in kernel.hyperparameters:
    print(hyperparameter)

params = kernel.get_params()
for key in sorted(params):
    print("%s : %s" % (key, params[key]))

print(kernel.theta)  # Note: log-transformed
print(kernel.bounds)  # Note: log-transformed
