import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

def definir_ab4():
    A = np.array([0, 0, 1])
    B = np.array([[1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0]])
    return A, B

def mostrar_molecula(ax, A, B, title='Geometría de la molécula AB4', plano=None):
    ax.clear()
    ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2]); ax.set_zlim([-1, 3])
    ax.set_box_aspect([1,1,1])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])

    if plano:
        x, z = np.linspace(-2, 2, 20), np.linspace(-1, 3, 20)
        X, Z = np.meshgrid(x, z)
        if plano == 'eje_z':
            z_line = np.linspace(-1, 3, 100)
            ax.plot(np.zeros_like(z_line), np.zeros_like(z_line), z_line, color='orange', linewidth=5)
        elif plano == 'diag1':
            ax.plot_surface(X, X, Z, alpha=0.3, color='green')
        elif plano == 'diag2':
            ax.plot_surface(X, -X, Z, alpha=0.3, color='purple')
        elif plano == 'yz':
            Y, Z_yz = np.meshgrid(np.linspace(-2, 2, 20), z)
            ax.plot_surface(np.zeros_like(Y), Y, Z_yz, alpha=0.3, color='blue')
        elif plano == 'xz':
            ax.plot_surface(X, np.zeros_like(X), Z, alpha=0.3, color='red')

    ax.plot([-2, 2], [0, 0], [0, 0], 'k--', alpha=0.5, linewidth=1)
    ax.plot([0, 0], [-2, 2], [0, 0], 'k--', alpha=0.5, linewidth=1)
    ax.plot([0, 0], [0, 0], [-1, 3], 'k--', alpha=0.5, linewidth=1)
    ax.text(2.2, 0, 0, 'X', fontsize=12, color='black', weight='bold')
    ax.text(0, 2.2, 0, 'Y', fontsize=12, color='black', weight='bold')
    ax.text(0, 0, 3.2, 'Z', fontsize=12, color='black', weight='bold')

    ax.scatter(A[0], A[1], A[2], color='green', s=250, label='Átomo A')
    ax.text(A[0]+0.1, A[1]+0.1, A[2]+0.1, 'A', fontsize=10, color='black', weight='bold')

    azules = ['blue', 'deepskyblue', 'dodgerblue', 'steelblue']
    for i in range(len(B)):
        ax.scatter(B[i,0], B[i,1], B[i,2], color=azules[i], s=150, label=f'Átomo B{i+1}')
        ax.text(B[i,0]+0.1, B[i,1]+0.1, B[i,2]+0.1, f'B{i+1}', fontsize=10, color='black', weight='bold')
    for b in B:
        ax.plot([A[0], b[0]], [A[1], b[1]], [A[2], b[2]], color='gray')
    ax.legend(loc='upper left'); ax.set_title(title)

def rotacion_c4(coords):
    theta = np.pi/2
    R = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    return coords @ R.T

def reflexion_sigmav1(coords):
    res = coords.copy(); res[1], res[3] = coords[3], coords[1]; return res

def reflexion_sigmav2(coords):
    res = coords.copy(); res[0], res[2] = coords[2], coords[0]; return res

def reflexion_sigmad1(coords):
    res = coords.copy(); res[0], res[1] = coords[1], coords[0]; res[2], res[3] = coords[3], coords[2]; return res

def reflexion_sigmad2(coords):
    res = coords.copy(); res[0], res[3] = coords[3], coords[0]; res[1], res[2] = coords[2], coords[1]; return res

def reflexion_sigmav_xz(coords):
    res = coords.copy(); res[0], res[3] = coords[3], coords[0]; res[1], res[2] = coords[2], coords[1]; return res

def reflexion_sigmav_yz(coords):
    res = coords.copy(); res[0], res[1] = coords[1], coords[0]; res[2], res[3] = coords[3], coords[2]; return res


def mostrar_molecula_sin_leyenda(ax, A, B, title='', plano=None, mostrar_leyenda=False):
    ax.clear()
    ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2]); ax.set_zlim([-1, 3])
    ax.set_box_aspect([1,1,1])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])

    if plano:
        x, z = np.linspace(-2, 2, 20), np.linspace(-1, 3, 20)
        X, Z = np.meshgrid(x, z)
        if plano == 'eje_z':
            z_line = np.linspace(-1, 3, 100)
            ax.plot(np.zeros_like(z_line), np.zeros_like(z_line), z_line, color='orange', linewidth=5)
        elif plano == 'diag1':
            ax.plot_surface(X, X, Z, alpha=0.3, color='green')
        elif plano == 'diag2':
            ax.plot_surface(X, -X, Z, alpha=0.3, color='purple')
        elif plano == 'yz':
            Y, Z_yz = np.meshgrid(np.linspace(-2, 2, 20), z)
            ax.plot_surface(np.zeros_like(Y), Y, Z_yz, alpha=0.3, color='blue')
        elif plano == 'xz':
            ax.plot_surface(X, np.zeros_like(X), Z, alpha=0.3, color='red')

    ax.plot([-2, 2], [0, 0], [0, 0], 'k--', alpha=0.5, linewidth=1)
    ax.plot([0, 0], [-2, 2], [0, 0], 'k--', alpha=0.5, linewidth=1)
    ax.plot([0, 0], [0, 0], [-1, 3], 'k--', alpha=0.5, linewidth=1)
    ax.text(2.2, 0, 0, 'X', fontsize=12, color='black', weight='bold')
    ax.text(0, 2.2, 0, 'Y', fontsize=12, color='black', weight='bold')
    ax.text(0, 0, 3.2, 'Z', fontsize=12, color='black', weight='bold')

    ax.scatter(A[0], A[1], A[2], color='green', s=250, label='Átomo A')
    ax.text(A[0]+0.1, A[1]+0.1, A[2]+0.1, 'A', fontsize=10, color='black', weight='bold')

    azules = ['blue', 'deepskyblue', 'dodgerblue', 'steelblue']
    for i in range(len(B)):
        ax.scatter(B[i,0], B[i,1], B[i,2], color=azules[i], s=150, label=f'Átomo B{i+1}')
        ax.text(B[i,0]+0.1, B[i,1]+0.1, B[i,2]+0.1, f'B{i+1}', fontsize=10, color='black', weight='bold')
    for b in B:
        ax.plot([A[0], b[0]], [A[1], b[1]], [A[2], b[2]], color='gray')
    if mostrar_leyenda:
        ax.legend(loc='upper left')
    ax.set_title(title)


def guardar_movimientos_subplot():
    carpeta = 'simetrias'
    os.makedirs(carpeta, exist_ok=True)
    fig = plt.figure(figsize=(16, 8))
    A, B = definir_ab4()

    axs = []
    for i in range(2):
        for j in range(4):
            axs.append(fig.add_subplot(2, 4, i*4 + j + 1, projection='3d'))

    B_e = B.copy()
    mostrar_molecula_sin_leyenda(axs[0], A, B_e, title='Identidad (E)', plano=None, mostrar_leyenda=True)

    B_c4_1 = rotacion_c4(B_e)
    mostrar_molecula_sin_leyenda(axs[1], A, B_c4_1, title='Rotación C4¹', plano='eje_z')

    B_c4_2 = rotacion_c4(B_c4_1)
    mostrar_molecula_sin_leyenda(axs[2], A, B_c4_2, title='Rotación C2 (C4²)', plano='eje_z')

    B_c4_3 = rotacion_c4(B_c4_2)
    mostrar_molecula_sin_leyenda(axs[3], A, B_c4_3, title='Rotación C4³', plano='eje_z')

    B_v1 = reflexion_sigmav_xz(B_e)
    mostrar_molecula_sin_leyenda(axs[4], A, B_v1, title='Reflexión σv1', plano='xz')

    B_v2 = reflexion_sigmav_yz(B_e)
    mostrar_molecula_sin_leyenda(axs[5], A, B_v2, title='Reflexión σv2', plano='yz')

    B_b1 = reflexion_sigmav1(B_e)
    mostrar_molecula_sin_leyenda(axs[6], A, B_b1, title='Reflexión σb1', plano='diag1')

    B_b2 = reflexion_sigmav2(B_e)
    mostrar_molecula_sin_leyenda(axs[7], A, B_b2, title='Reflexión σb2', plano='diag2')

    plt.tight_layout()
    nombre_archivo = f"{carpeta}/simetrias_subplot.png"
    plt.savefig(nombre_archivo)
    print(f"Guardado: {nombre_archivo}")
    plt.close(fig)

if __name__ == "__main__":
    guardar_movimientos_subplot()
