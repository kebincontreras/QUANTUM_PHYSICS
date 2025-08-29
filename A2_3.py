import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

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

def animacion_simetria_final():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    A, B = definir_ab4()

    operaciones = [
        ('Identidad (E)', lambda c: c, None),
        ('Rotación C4¹ (90°)', rotacion_c4, 'eje_z'),
        ('Rotación C4² (180°)', rotacion_c4, 'eje_z'),
        ('Rotación C4³ (270°)', rotacion_c4, 'eje_z'),
        ('Rotación C4⁴ (360°=E)', rotacion_c4, 'eje_z'),
        ('Reflexión σv1 (plano xz)', reflexion_sigmav_xz, 'xz'),
        ('Reflexión σv2 (plano yz)', reflexion_sigmav_yz, 'yz'),
        ('Reflexión σb1 (B1,B3 fijos)', reflexion_sigmav1, 'diag1'),
        ('Reflexión σb2 (B2,B4 fijos)', reflexion_sigmav2, 'diag2')
    ]

    posiciones_finales = []
    B_acumulado = B.copy()
    for op_name, op_func, plano in operaciones:
        B_acumulado = op_func(B_acumulado)
        posiciones_finales.append((op_name, B_acumulado, plano))

    frames_por_transicion, frames_pausa = 40, 25
    total_frames = len(operaciones) * (frames_por_transicion + frames_pausa)

    def update(frame):
        ciclo_frame = frame % total_frames
        op_idx = ciclo_frame // (frames_por_transicion + frames_pausa)
        frame_en_op = ciclo_frame % (frames_por_transicion + frames_pausa)
        
        op_name, B_final, plano = posiciones_finales[op_idx]
        
        if op_idx == 0:
            B_inicial = B.copy()
        elif 'Reflexión' in op_name and 'Rotación' in operaciones[op_idx-1][0]:
            B_inicial = B.copy()
        else:
            _, B_inicial, _ = posiciones_finales[op_idx - 1]

        if frame_en_op < frames_por_transicion:
            t = 0.5 * (1 - np.cos(np.pi * (frame_en_op / frames_por_transicion)))
            B_actual = B_inicial + t * (B_final - B_inicial)
            titulo = f'Transición: {op_name}'
        else:
            B_actual = B_final
            titulo = f'Operación: {op_name}'
        
        mostrar_molecula(ax, A, B_actual, title=titulo, plano=plano)

    ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=50, repeat=True)
    
    plt.show()

animacion_simetria_final()
