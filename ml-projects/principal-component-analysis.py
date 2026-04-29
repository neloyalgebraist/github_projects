import utils
import numpy as np 
imgs = utils.load_images('./data/')

height, width = img[0].shape
print(f'\nYour dataset has {len(imgs)} images of size {height}x{width} pixels\n')
plt.imshow(imgs[0], cmap='grey')

imgs_flatten = np.array([im.reshape(-1) for im in imgs])

print(f'imgs_flatten shape: {imgs_flatten.shape}')

def center_data(Y):
    """
    Center your original data
    Args:
        Y (ndarray): input data. Shape (n_observations x n_pixels)

    Outputs:
        X (ndarray): centered data 
    """
    mean_vector = np.mean(Y, axis=0)
    mean_matrix = np.repeat(mean_vector, 55)
    mean_matrix = mean_matrix.reshape((55,4096), order='F')
    
    X = Y - mean_matrix

    return X 

X = center_data(imgs_flatten)
plt.imshow(X[0].reshape(64,64), cmap='gray')

def get_cov_matrix(X):
    """
    Calculate covariance matrix from the centered data X

    Args:
        X (np.array): centered data matrix 
    Outputs:
        cov_matrix (np.ndarray): covariance matrix 
    """
    cov_matrix = (1/(len(X)-1)) * np.dot(X.T, X)

    return cov_matrix

cov_matrix = get_cov_matrix(X)

print(f'Covariance matrix shape: {cov_matrix.shape}')

scipy.random.seed(7)
eigenvals, eigenvecs = scipy.sparse.linalg.eigsh(cov_matrix, k=55)
print(f'Ten largest eigenvalues: \n{eigenvals[-10]}')

eigenvls = eigenvals[::-1]
eigenvecs = eigenvecs[:,::-1]
print(f'Ten largest eigenvalues: \n{eigenvals[:10]}')

fig, ax = plt.subplots(4,4, figsize=(20,20))
for n in range(4):
    for k in range(4):
        ax[n,k].imshow(eigvecs[:,n*4+k].reshape(height,width), cmap='gray')
        ax[n,k].set_title(f'component number {n*4+k+1}')

    def perform_PCA(X, eigenvecs, k):
        """
        Perform dimensionality reduction with perform_PCA
        Inputs:
            X (ndarray): original data matrix. Has dimensions (n_observations)x(n_variables)
            eigenvecs (ndarray): matrix of eigenvectors. Each column is one eigenvector. The k-th eigenvector
                                is associated to the k-th eigenvalue 
            k (int): number of principal components to use 

        Returns: 
            Xred

        """

        V = eigenvecs[:,:k]
        Xred = np.dot(X,V)
        return Xred

    Xred2 = perform_PCA(X,eigenvecs,2)
    print(f'Xred2 shape: {Xred2.shape}')

    def reconstruct_image(Xred, eigenvecs):
        X_reconstructed = Xred.dot(eigenvecs[:,:Xred.shape[1]].T)

        return X_reconstructed

    explained_variance = eigenvals/sum(eigenvals)
    plt.plot(np.arange(1,56), explained_variance)

    explained_cum_variance = np.cumsum(explained_variance)
    plt.plot(np.arange(1,56), explained_cum_variance)
    plt.axhline(y=0.95, color='r')


