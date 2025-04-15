import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, 
                              QPushButton, QComboBox, QGroupBox, QCheckBox)
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint

class Letter3D:
    def __init__(self, letter, height=4, width=2, depth=1):
        self.letter = letter
        self.height = height
        self.width = width
        self.depth = depth
        self.position = [0, 0, 0]  # Позиция в глобальных координатах
        self.rotation = [0, 0, 0]  # Углы поворота в градусах (вокруг глобальных осей)
        self.scale = [1, 1, 1]  # Масштаб по глобальным осям
        self.reflection = [1, 1, 1]  # Отражение по глобальным осям
        self.vertices = []  # Вершины в локальных координатах
        self.transformed_vertices = []  # Вершины в глобальных координатах
        self.edges = []
        self.faces = []
        self.update_geometry()
    
    def transform_vertex(self, vertex):
        """Преобразует вершину из локальных координат в глобальные"""
        # Применяем масштаб и отражение
        transformed = [
            vertex[0] * self.scale[0] * self.reflection[0],
            vertex[1] * self.scale[1] * self.reflection[1],
            vertex[2] * self.scale[2] * self.reflection[2]
        ]
        
        # Поворот вокруг глобальной оси X
        angle_x = math.radians(self.rotation[0])
        y = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y, z]
        
        # Поворот вокруг глобальной оси Y
        angle_y = math.radians(self.rotation[1])
        x = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x, transformed[1], z]
        
        # Поворот вокруг глобальной оси Z
        angle_z = math.radians(self.rotation[2])
        x = transformed[0] * math.cos(angle_z) - transformed[1] * math.sin(angle_z)
        y = transformed[0] * math.sin(angle_z) + transformed[1] * math.cos(angle_z)
        transformed = [x, y, transformed[2]]
        
        # Применяем перемещение в глобальных координатах
        return [
            transformed[0] + self.position[0],
            transformed[1] + self.position[1],
            transformed[2] + self.position[2]
        ]

    def update_geometry(self):
        if self.letter == 'D':
            self.create_letter_d()
        # После создания геометрии обновляем трансформированные вершины
        self.transformed_vertices = [self.transform_vertex(v) for v in self.vertices]
    
    def create_letter_d(self):
        self.vertices = []
        self.edges = []
        self.faces = []
        
        # Внешний контур - передняя часть
        front_outer = [
            [0, 0, 0],
            [0, self.height, 0],
            [self.width, self.height * 0.75, 0],
            [self.width, self.height * 0.25, 0]
        ]
        
        # Внутренний контур - передняя часть
        front_inner = [
            [self.width * 0.3, self.height * 0.25, 0],
            [self.width * 0.3, self.height * 0.75, 0],
            [self.width * 0.8, self.height * 0.65, 0],
            [self.width * 0.8, self.height * 0.35, 0]
        ]
        
        # Создаем заднюю часть
        back_outer = [[v[0], v[1], v[2] + self.depth] for v in front_outer]
        back_inner = [[v[0], v[1], v[2] + self.depth] for v in front_inner]
        
        # Сохраняем вершины в локальных координатах
        self.vertices = front_outer + front_inner + back_outer + back_inner

        # Функция для добавления ребра
        def add_edge(v1_idx, v2_idx):
            edge = (min(v1_idx, v2_idx), max(v1_idx, v2_idx))
            if edge not in self.edges:
                self.edges.append(edge)

        # Добавляем ребра для внешнего контура (спереди)
        for i in range(len(front_outer)):
            add_edge(i, (i + 1) % len(front_outer))

        # Добавляем ребра для внутреннего контура (спереди)
        for i in range(len(front_inner)):
            add_edge(i + len(front_outer), 
                    ((i + 1) % len(front_inner)) + len(front_outer))

        # Добавляем ребра для внешнего контура (сзади)
        for i in range(len(back_outer)):
            add_edge(i + len(front_outer) * 2, 
                    ((i + 1) % len(back_outer)) + len(front_outer) * 2)

        # Добавляем ребра для внутреннего контура (сзади)
        for i in range(len(back_inner)):
            add_edge(i + len(front_outer) * 3, 
                    ((i + 1) % len(back_inner)) + len(front_outer) * 3)

        # Добавляем соединяющие ребра между передней и задней частью (внешний контур)
        for i in range(len(front_outer)):
            add_edge(i, i + len(front_outer) * 2)

        # Добавляем соединяющие ребра между передней и задней частью (внутренний контур)
        for i in range(len(front_inner)):
            add_edge(i + len(front_outer), i + len(front_outer) * 3)

        # Добавляем соединяющие ребра между внешним и внутренним контуром (спереди)
        for i in range(len(front_outer)):
            add_edge(i, i + len(front_outer))

        # Добавляем соединяющие ребра между внешним и внутренним контуром (сзади)
        for i in range(len(back_outer)):
            add_edge(i + len(front_outer) * 2, i + len(front_outer) * 3)

        # Создаем грани
        # Передняя грань (внешняя)
        self.faces.append({
            'vertices': front_outer,
            'edges': [(i, (i + 1) % len(front_outer)) for i in range(len(front_outer))],
            'normal': [0, 0, -1]
        })
        
        # Передняя грань (внутренняя)
        self.faces.append({
            'vertices': list(reversed(front_inner)),
            'edges': [(i + len(front_outer), ((i + 1) % len(front_inner)) + len(front_outer)) 
                     for i in range(len(front_inner))],
            'normal': [0, 0, -1]
        })
        
        # Задняя грань (внешняя)
        self.faces.append({
            'vertices': list(reversed(back_outer)),
            'edges': [(i + len(front_outer) * 2, ((i + 1) % len(back_outer)) + len(front_outer) * 2) 
                     for i in range(len(back_outer))],
            'normal': [0, 0, 1]
        })
        
        # Задняя грань (внутренняя)
        self.faces.append({
            'vertices': back_inner,
            'edges': [(i + len(front_outer) * 3, ((i + 1) % len(back_inner)) + len(front_outer) * 3) 
                     for i in range(len(back_inner))],
            'normal': [0, 0, 1]
        })

    def reflect(self, axis):
        if axis == 'x':
            self.reflection[0] = -self.reflection[0]
        elif axis == 'y':
            self.reflection[1] = -self.reflection[1]
        elif axis == 'z':
            self.reflection[2] = -self.reflection[2]
        self.update_geometry()

    def rotate(self, axis, angle):
        if axis == 'x':
            self.rotation[0] += angle
        elif axis == 'y':
            self.rotation[1] += angle
        elif axis == 'z':
            self.rotation[2] += angle
        self.update_geometry()

    def scale_object(self, axis, factor):
        if axis == 'x':
            self.scale[0] *= factor
        elif axis == 'y':
            self.scale[1] *= factor
        elif axis == 'z':
            self.scale[2] *= factor
        self.update_geometry()

    def set_uniform_scale(self, scale):
        self.scale = [scale, scale, scale]
        self.update_geometry()

class ViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.letters = []
        self.camera_pos = [0, 0, -10]
        self.camera_rot = [0, 0, 0]
        self.last_pos = QPoint()
        self.mouse_pressed = False
        self.scale = 40
        self.selected_letter = None
        self.grid_size = 10
        self.movement_step = 0.5  # Шаг перемещения для кнопок
        self.rotation_step = 5  # Начальный шаг поворота в градусах
        
        # Добавляем буквы
        self.add_letter('D', 4, 2, 1)
    
    def add_letter(self, letter, height, width, depth):
        new_letter = Letter3D(letter, height, width, depth)
        self.letters.append(new_letter)
        if not self.selected_letter:
            self.selected_letter = new_letter
    
    def project_point(self, point, is_grid=False):
        """Проецирует точку из глобальных координат на экран"""
        if is_grid:
            transformed = point.copy()
        else:
            # Точка уже в глобальных координатах
            transformed = point.copy()
        
        # Поворот камеры
        angle_y = math.radians(self.camera_rot[1])
        angle_x = math.radians(self.camera_rot[0])
        
        # Поворот вокруг Y
        x_rot = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z_rot = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x_rot, transformed[1], z_rot]
        
        # Поворот вокруг X
        y_rot = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z_rot = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y_rot, z_rot]
        
        # Перспективная проекция
        f = 500  # фокусное расстояние
        z = transformed[2] - self.camera_pos[2]
        if z + f != 0:
            scale_factor = f / (z + f)
            screen_x = transformed[0] * scale_factor * self.scale + self.width() / 2
            screen_y = transformed[1] * scale_factor * self.scale + self.height() / 2
            return QPoint(int(screen_x), int(screen_y))
        return None

    def draw_grid(self, painter):
        # Рисуем сетку
        grid_color = QColor(80, 80, 80)  # Увеличиваем яркость сетки
        axis_color = QColor(120, 120, 120)  # Увеличиваем яркость осей
        
        # Рисуем горизонтальные линии
        for i in range(-self.grid_size, self.grid_size + 1):
            for j in range(-self.grid_size, self.grid_size + 1):
                start = [i, 0, j]
                
                # Линии параллельные оси X
                end = [i, 0, j + 1]
                start_screen = self.project_point(start, is_grid=True)
                end_screen = self.project_point(end, is_grid=True)
                if start_screen and end_screen:
                    painter.setPen(QPen(axis_color if i == 0 or j == 0 else grid_color, 1))
                    painter.drawLine(start_screen, end_screen)
                
                # Линии параллельные оси Z
                end = [i + 1, 0, j]
                end_screen = self.project_point(end, is_grid=True)
                if start_screen and end_screen:
                    painter.setPen(QPen(axis_color if i == 0 or j == 0 else grid_color, 1))
                    painter.drawLine(start_screen, end_screen)

    def draw_axes(self, painter):
        # Рисуем оси координат
        origin = self.project_point([0, 0, 0], is_grid=True)
        if origin:
            # Ось X (красная)
            end = self.project_point([5, 0, 0], is_grid=True)
            if end:
                painter.setPen(QPen(Qt.red, 2))
                painter.drawLine(origin, end)
            
            # Ось Y (зеленая)
            end = self.project_point([0, 5, 0], is_grid=True)
            if end:
                painter.setPen(QPen(Qt.green, 2))
                painter.drawLine(origin, end)
            
            # Ось Z (синяя)
            end = self.project_point([0, 0, 5], is_grid=True)
            if end:
                painter.setPen(QPen(Qt.blue, 2))
                painter.drawLine(origin, end)

    def get_face_depth(self, face, letter):
        # Вычисляем среднюю Z-координату грани после всех преобразований
        z_sum = 0
        for vertex in face['vertices']:
            # Применяем позицию объекта
            transformed = [vertex[0] + letter.position[0], vertex[1] + letter.position[1], vertex[2] + letter.position[2]]
            
            # Поворот камеры
            angle_y = math.radians(self.camera_rot[1])
            angle_x = math.radians(self.camera_rot[0])
            
            # Поворот вокруг Y
            x_rot = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
            z_rot = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
            transformed = [x_rot, transformed[1], z_rot]
            
            # Поворот вокруг X
            y_rot = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
            z_rot = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
            
            z_sum += z_rot
        
        return z_sum / len(face['vertices'])

    def is_face_visible(self, face, letter):
        # Вычисляем нормаль грани в мировых координатах с учетом поворота камеры
        normal = face['normal']
        
        # Вычисляем вектор направления взгляда (от точки на грани к камере)
        center = [0, 0, 0]
        for vertex in face['vertices']:
            center[0] += vertex[0] + letter.position[0]
            center[1] += vertex[1] + letter.position[1]
            center[2] += vertex[2] + letter.position[2]
        center[0] /= len(face['vertices'])
        center[1] /= len(face['vertices'])
        center[2] /= len(face['vertices'])
        
        view_dir = [self.camera_pos[0] - center[0], self.camera_pos[1] - center[1], self.camera_pos[2] - center[2]]
        view_dir[0] /= math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        view_dir[1] /= math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        view_dir[2] /= math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        
        # Грань видима, если угол между нормалью и направлением взгляда меньше 90 градусов
        dot_product = normal[0] * view_dir[0] + normal[1] * view_dir[1] + normal[2] * view_dir[2]
        return dot_product > 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Черный фон
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        # Рисуем сетку и оси
        self.draw_grid(painter)
        self.draw_axes(painter)
        
        # Рисуем каждую букву
        for letter in self.letters:
            # Рисуем все ребра
            painter.setPen(QPen(Qt.white, 2))
            for edge in letter.edges:
                # Используем уже трансформированные вершины
                v1 = letter.transformed_vertices[edge[0]]
                v2 = letter.transformed_vertices[edge[1]]
                
                p1 = self.project_point(v1)
                p2 = self.project_point(v2)
                
                if p1 and p2:
                    painter.drawLine(p1, p2)

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if not self.mouse_pressed:
            return
            
        current_pos = event.pos()
        dx = current_pos.x() - self.last_pos.x()
        dy = current_pos.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:  # Вращение камеры
            self.camera_rot[1] += dx * 0.5
            self.camera_rot[0] += dy * 0.5
        elif event.buttons() & Qt.RightButton:  # Перемещение объекта по глобальным осям
            if self.selected_letter:
                if event.modifiers() & Qt.ShiftModifier:  # Перемещение по глобальной Y (вперед/назад)
                    self.selected_letter.position[1] += dy * 0.1
                elif event.modifiers() & Qt.ControlModifier:  # Перемещение по глобальной Z (вверх/вниз)
                    self.selected_letter.position[2] -= dy * 0.1
                else:  # Перемещение по глобальной X (влево/вправо)
                    self.selected_letter.position[0] += dx * 0.1
        
        self.last_pos = current_pos
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.scale *= pow(1.001, delta)
        self.update()

    def move_selected(self, axis, direction):
        """Перемещение объекта по глобальным осям координат"""
        if self.selected_letter:
            step = direction * self.movement_step
            if axis == 'x':  # Перемещение по глобальной оси X (влево/вправо)
                self.selected_letter.position[0] += step
            elif axis == 'y':  # Перемещение по глобальной оси Y (вперед/назад)
                self.selected_letter.position[1] += step
            elif axis == 'z':  # Перемещение по глобальной оси Z (вверх/вниз)
                self.selected_letter.position[2] += step
            self.update()

    def reflect_selected(self, axis):
        if self.selected_letter:
            self.selected_letter.reflect(axis)
            self.update()

    def rotate_selected(self, axis, direction):
        if self.selected_letter:
            self.selected_letter.rotate(axis, direction * self.rotation_step)
            self.update()

    def scale_selected(self, axis, direction):
        if self.selected_letter:
            factor = self.scale_step if direction > 0 else 1 / self.scale_step
            self.selected_letter.scale_object(axis, factor)
            self.update()

    def set_rotation_step(self, value):
        self.rotation_step = value

    def set_uniform_scale(self, scale):
        if self.selected_letter:
            self.selected_letter.set_uniform_scale(scale)
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Viewer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Создаем главный виджет и layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Создаем область для 3D просмотра
        self.viewer = ViewerWidget()
        main_layout.addWidget(self.viewer, stretch=2)
        
        # Создаем панель управления
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        main_layout.addWidget(control_panel, stretch=1)
        
        # Группа параметров буквы
        letter_group = QGroupBox("Параметры буквы")
        letter_layout = QVBoxLayout(letter_group)
        
        # Высота
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Высота:"))
        height_spin = QDoubleSpinBox()
        height_spin.setRange(0.1, 20.0)
        height_spin.setValue(4.0)
        height_spin.valueChanged.connect(self.update_letter_params)
        height_layout.addWidget(height_spin)
        letter_layout.addLayout(height_layout)
        
        # Ширина
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Ширина:"))
        width_spin = QDoubleSpinBox()
        width_spin.setRange(0.1, 20.0)
        width_spin.setValue(2.0)
        width_spin.valueChanged.connect(self.update_letter_params)
        width_layout.addWidget(width_spin)
        letter_layout.addLayout(width_layout)
        
        # Глубина
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Глубина:"))
        depth_spin = QDoubleSpinBox()
        depth_spin.setRange(0.1, 20.0)
        depth_spin.setValue(1.0)
        depth_spin.valueChanged.connect(self.update_letter_params)
        depth_layout.addWidget(depth_spin)
        letter_layout.addLayout(depth_layout)

        # Группа управления перемещением
        movement_group = QGroupBox("Управление перемещением")
        movement_layout = QVBoxLayout(movement_group)

        # Шаг перемещения
        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel("Шаг:"))
        step_spin = QDoubleSpinBox()
        step_spin.setRange(0.1, 5.0)
        step_spin.setValue(0.5)
        step_spin.setSingleStep(0.1)
        step_spin.valueChanged.connect(self.update_movement_step)
        step_layout.addWidget(step_spin)
        movement_layout.addLayout(step_layout)

        # Кнопки перемещения по X
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X (влево/вправо):"))
        x_minus = QPushButton("-X")
        x_minus.clicked.connect(lambda: self.viewer.move_selected('x', -1))
        x_plus = QPushButton("+X")
        x_plus.clicked.connect(lambda: self.viewer.move_selected('x', 1))
        x_layout.addWidget(x_minus)
        x_layout.addWidget(x_plus)
        movement_layout.addLayout(x_layout)

        # Кнопки перемещения по Y
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y (вперед/назад):"))
        y_minus = QPushButton("-Y")
        y_minus.clicked.connect(lambda: self.viewer.move_selected('y', -1))
        y_plus = QPushButton("+Y")
        y_plus.clicked.connect(lambda: self.viewer.move_selected('y', 1))
        y_layout.addWidget(y_minus)
        y_layout.addWidget(y_plus)
        movement_layout.addLayout(y_layout)

        # Кнопки перемещения по Z
        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Z (вверх/вниз):"))
        z_minus = QPushButton("-Z")
        z_minus.clicked.connect(lambda: self.viewer.move_selected('z', -1))
        z_plus = QPushButton("+Z")
        z_plus.clicked.connect(lambda: self.viewer.move_selected('z', 1))
        z_layout.addWidget(z_minus)
        z_layout.addWidget(z_plus)
        movement_layout.addLayout(z_layout)

        # Группа управления вращением
        rotation_group = QGroupBox("Вращение объекта")
        rotation_layout = QVBoxLayout(rotation_group)

        # Добавляем спинбокс для шага поворота
        rotation_step_layout = QHBoxLayout()
        rotation_step_layout.addWidget(QLabel("Шаг поворота (градусы):"))
        rotation_step_spin = QSpinBox()
        rotation_step_spin.setRange(1, 90)
        rotation_step_spin.setValue(5)
        rotation_step_spin.valueChanged.connect(self.update_rotation_step)
        rotation_step_layout.addWidget(rotation_step_spin)
        rotation_layout.addLayout(rotation_step_layout)

        # Кнопки вращения вокруг X
        x_rot_layout = QHBoxLayout()
        x_rot_layout.addWidget(QLabel("Вращение X:"))
        x_rot_minus = QPushButton("-X")
        x_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('x', -1))
        x_rot_plus = QPushButton("+X")
        x_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('x', 1))
        x_rot_layout.addWidget(x_rot_minus)
        x_rot_layout.addWidget(x_rot_plus)
        rotation_layout.addLayout(x_rot_layout)

        # Кнопки вращения вокруг Y
        y_rot_layout = QHBoxLayout()
        y_rot_layout.addWidget(QLabel("Вращение Y:"))
        y_rot_minus = QPushButton("-Y")
        y_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('y', -1))
        y_rot_plus = QPushButton("+Y")
        y_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('y', 1))
        y_rot_layout.addWidget(y_rot_minus)
        y_rot_layout.addWidget(y_rot_plus)
        rotation_layout.addLayout(y_rot_layout)

        # Кнопки вращения вокруг Z
        z_rot_layout = QHBoxLayout()
        z_rot_layout.addWidget(QLabel("Вращение Z:"))
        z_rot_minus = QPushButton("-Z")
        z_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('z', -1))
        z_rot_plus = QPushButton("+Z")
        z_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('z', 1))
        z_rot_layout.addWidget(z_rot_minus)
        z_rot_layout.addWidget(z_rot_plus)
        rotation_layout.addLayout(z_rot_layout)

        # Группа управления отражением
        reflection_group = QGroupBox("Отражение")
        reflection_layout = QVBoxLayout(reflection_group)

        # Кнопки отражения
        x_reflect = QPushButton("Отражение по X")
        x_reflect.clicked.connect(lambda: self.viewer.reflect_selected('x'))
        reflection_layout.addWidget(x_reflect)

        y_reflect = QPushButton("Отражение по Y")
        y_reflect.clicked.connect(lambda: self.viewer.reflect_selected('y'))
        reflection_layout.addWidget(y_reflect)

        z_reflect = QPushButton("Отражение по Z")
        z_reflect.clicked.connect(lambda: self.viewer.reflect_selected('z'))
        reflection_layout.addWidget(z_reflect)

        # Группа управления масштабом
        scale_group = QGroupBox("Масштаб")
        scale_layout = QVBoxLayout(scale_group)

        # Бегунок масштаба
        scale_layout.addWidget(QLabel("Масштаб:"))
        scale_spin = QDoubleSpinBox()
        scale_spin.setRange(0.1, 10.0)
        scale_spin.setValue(1.0)
        scale_spin.setSingleStep(0.1)
        scale_spin.valueChanged.connect(lambda v: self.viewer.set_uniform_scale(v))
        scale_layout.addWidget(scale_spin)

        # Добавляем группы в панель управления
        control_layout.addWidget(letter_group)
        control_layout.addWidget(movement_group)
        control_layout.addWidget(rotation_group)
        control_layout.addWidget(scale_group)
        control_layout.addWidget(reflection_group)
        
        # Добавляем подсказки по управлению
        help_text = QLabel(
            "Управление:\n"
            "ЛКМ - вращение камеры\n"
            "ПКМ - перемещение по X (влево/вправо)\n"
            "ПКМ + Shift - перемещение по Y (вперед/назад)\n"
            "ПКМ + Ctrl - перемещение по Z (вверх/вниз)\n"
            "Колесико - масштаб просмотра"
        )
        control_layout.addWidget(help_text)
        
        # Добавляем растягивающийся пробел
        control_layout.addStretch()
        
        # Сохраняем ссылки на спинбоксы
        self.height_spin = height_spin
        self.width_spin = width_spin
        self.depth_spin = depth_spin
        self.step_spin = step_spin
        self.rotation_step_spin = rotation_step_spin
        self.scale_spin = scale_spin

    def update_letter_params(self):
        if self.viewer.selected_letter:
            self.viewer.selected_letter.height = self.height_spin.value()
            self.viewer.selected_letter.width = self.width_spin.value()
            self.viewer.selected_letter.depth = self.depth_spin.value()
            self.viewer.selected_letter.update_geometry()
            self.viewer.update()

    def update_movement_step(self, value):
        self.viewer.movement_step = value

    def update_rotation_step(self, value):
        self.viewer.set_rotation_step(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 
