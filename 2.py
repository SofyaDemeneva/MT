import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, 
                              QPushButton, QComboBox, QGroupBox, QCheckBox)
from PySide6.QtGui import QPainter, QPen, QColor, QPolygon
from PySide6.QtCore import Qt, QPointimport sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                               QPushButton, QComboBox, QGroupBox, QCheckBox,
                               QScrollArea, QTabWidget)
from PySide6.QtGui import QPainter, QPen, QColor, QPolygon
from PySide6.QtCore import Qt, QPoint


class Letter3D:
    def __init__(self, letter, height=4, width=2, depth=1):
        self.letter = letter
        self.height = height
        self.width = width
        self.depth = depth
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.reflection = [1, 1, 1]
        self.vertices = []
        self.transformed_vertices = []
        self.edges = []
        self.faces = []
        self.center_point = [0, 0, 0]
        self.transformed_center_point = [0, 0, 0]
        self.show_center = True
        self.update_geometry()

    def transform_vertex(self, vertex):
        transformed = [
            vertex[0] * self.scale[0] * self.reflection[0],
            vertex[1] * self.scale[1] * self.reflection[1],
            vertex[2] * self.scale[2] * self.reflection[2]
        ]

        angle_x = math.radians(self.rotation[0])
        y = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y, z]

        angle_y = math.radians(self.rotation[1])
        x = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x, transformed[1], z]

        angle_z = math.radians(self.rotation[2])
        x = transformed[0] * math.cos(angle_z) - transformed[1] * math.sin(angle_z)
        y = transformed[0] * math.sin(angle_z) + transformed[1] * math.cos(angle_z)
        transformed = [x, y, transformed[2]]

        return [
            transformed[0] + self.position[0],
            transformed[1] + self.position[1],
            transformed[2] + self.position[2]
        ]

    def update_geometry(self):
        if self.letter == 'С':
            self.create_letter_c()
        elif self.letter == 'Д':
            self.create_letter_de()

        self.calculate_center_point()
        self.transformed_vertices = [self.transform_vertex(v) for v in self.vertices]
        self.transformed_center_point = self.transform_vertex(self.center_point)

    def calculate_center_point(self):
        # Геометрический центр всех вершин
        if not self.vertices:
            self.center_point = [0, 0, 0]
            return
        n = len(self.vertices)
        cx = sum(v[0] for v in self.vertices) / n
        cy = sum(v[1] for v in self.vertices) / n
        cz = sum(v[2] for v in self.vertices) / n
        self.center_point = [cx, cy, cz]

    def toggle_center_point(self):
        self.show_center = not self.show_center
        return self.show_center

    def create_letter_c(self):
        self.vertices = []
        self.edges = []
        self.faces = []

        h = self.height
        w = self.width
        d = self.depth
        t = w * 0.15

        segments = 12

        front_outer = []
        for i in range(segments + 1):
            angle = math.radians(110) - math.radians(220) * i / segments
            x = w * 0.6 + w * 0.4 * math.cos(angle)
            y = h * 0.5 + h * 0.5 * math.sin(angle)
            front_outer.append([x, y, 0])

        front_inner = []
        for i in range(segments + 1):
            angle = math.radians(110) - math.radians(220) * i / segments
            x = w * 0.6 + (w * 0.4 - t) * math.cos(angle)
            y = h * 0.5 + (h * 0.5 - t) * math.sin(angle)
            front_inner.append([x, y, 0])

        back_outer = [[v[0], v[1], v[2] + d] for v in front_outer]
        back_inner = [[v[0], v[1], v[2] + d] for v in front_inner]

        self.vertices = front_outer + front_inner + back_outer + back_inner

        def add_edge(v1, v2):
            edge = (min(v1, v2), max(v1, v2))
            if edge not in self.edges:
                self.edges.append(edge)

        for i in range(len(front_outer) - 1):
            add_edge(i, i + 1)

        inner_offset = len(front_outer)
        for i in range(len(front_inner) - 1):
            add_edge(inner_offset + i, inner_offset + i + 1)

        back_offset = inner_offset + len(front_inner)
        for i in range(len(back_outer) - 1):
            add_edge(back_offset + i, back_offset + i + 1)

        back_inner_offset = back_offset + len(back_outer)
        for i in range(len(back_inner) - 1):
            add_edge(back_inner_offset + i, back_inner_offset + i + 1)

        add_edge(0, back_offset)
        add_edge(len(front_outer) - 1, back_offset + len(back_outer) - 1)
        add_edge(inner_offset, back_inner_offset)
        add_edge(inner_offset + len(front_inner) - 1, back_inner_offset + len(back_inner) - 1)

        add_edge(0, inner_offset)
        add_edge(len(front_outer) - 1, inner_offset + len(front_inner) - 1)
        add_edge(back_offset, back_inner_offset)
        add_edge(back_offset + len(back_outer) - 1, back_inner_offset + len(back_inner) - 1)

        for i in range(segments + 1):
            add_edge(i, inner_offset + i)
            add_edge(back_offset + i, back_inner_offset + i)
            add_edge(i, back_offset + i)
            add_edge(inner_offset + i, back_inner_offset + i)

        self.faces = [
            {'vertices': front_outer, 'normal': [0, 0, -1]},
            {'vertices': front_inner, 'normal': [0, 0, 1]},
            {'vertices': [v for v in reversed(back_outer)], 'normal': [0, 0, 1]},
            {'vertices': [v for v in reversed(back_inner)], 'normal': [0, 0, -1]},
            {'vertices': [front_outer[0], front_inner[0], back_inner[0], back_outer[0]],
             'normal': [0, 1, 0]},
            {'vertices': [front_outer[-1], front_inner[-1], back_inner[-1], back_outer[-1]],
             'normal': [0, -1, 0]},
        ]

    def create_letter_de(self):
        self.vertices = []
        self.edges = []
        self.faces = []

        h = self.height
        w = self.width
        d = self.depth
        leg_h = h * 0.15
        leg_w = w * 0.1
        t = w * 0.15

        front_outer = [
            [-leg_w, -leg_h, 0],
            [w + leg_w, -leg_h, 0],
            [w + leg_w, 0, 0],
            [w, 0, 0],
            [w, h - t, 0],
            [0, h - t, 0],
            [0, 0, 0],
            [-leg_w, 0, 0]
        ]

        front_roof = [
            [0, h - t, 0],
            [w, h - t, 0],
            [w - t, h, 0],
            [t, h, 0]
        ]

        front_inner = [
            [t, t, 0],
            [w - t, t, 0],
            [w - t, h - t * 2, 0],
            [t, h - t * 2, 0]
        ]

        back_outer = [[v[0], v[1], v[2] + d] for v in front_outer]
        back_roof = [[v[0], v[1], v[2] + d] for v in front_roof]
        back_inner = [[v[0], v[1], v[2] + d] for v in front_inner]

        self.vertices = front_outer + front_roof + front_inner + back_outer + back_roof + back_inner

        def add_edge(v1_idx, v2_idx):
            edge = (min(v1_idx, v2_idx), max(v1_idx, v2_idx))
            if edge not in self.edges:
                self.edges.append(edge)

        for i in range(len(front_outer)):
            add_edge(i, (i + 1) % len(front_outer))

        roof_offset = len(front_outer)
        for i in range(len(front_roof)):
            add_edge(roof_offset + i, roof_offset + (i + 1) % len(front_roof))

        inner_offset = roof_offset + len(front_roof)
        for i in range(len(front_inner)):
            add_edge(inner_offset + i, inner_offset + (i + 1) % len(front_inner))

        back_offset = inner_offset + len(front_inner)
        for i in range(len(back_outer)):
            add_edge(back_offset + i, back_offset + (i + 1) % len(back_outer))

        back_roof_offset = back_offset + len(back_outer)
        for i in range(len(back_roof)):
            add_edge(back_roof_offset + i, back_roof_offset + (i + 1) % len(back_roof))

        back_inner_offset = back_roof_offset + len(back_roof)
        for i in range(len(back_inner)):
            add_edge(back_inner_offset + i, back_inner_offset + (i + 1) % len(back_inner))

        for i in range(len(front_outer)):
            add_edge(i, back_offset + i)

        for i in range(len(front_roof)):
            add_edge(roof_offset + i, back_roof_offset + i)

        for i in range(len(front_inner)):
            add_edge(inner_offset + i, back_inner_offset + i)

        add_edge(5, roof_offset)
        add_edge(4, roof_offset + 1)
        add_edge(back_offset + 5, back_roof_offset)
        add_edge(back_offset + 4, back_roof_offset + 1)

        self.faces = [
            {'vertices': front_outer, 'normal': [0, 0, -1]},
            {'vertices': front_roof, 'normal': [0, 0, -1]},
            {'vertices': front_inner, 'normal': [0, 0, 1]},
            {'vertices': back_outer, 'normal': [0, 0, 1]},
            {'vertices': back_roof, 'normal': [0, 0, 1]},
            {'vertices': back_inner, 'normal': [0, 0, -1]},
        ]

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
        self.camera_rot = [-30, 0, 0]
        self.last_pos = QPoint()
        self.mouse_pressed = False
        self.scale = 40
        self.selected_letter = None
        self.grid_size = 10
        self.movement_step = 0.5
        self.rotation_step = 5

        self.render_mode = "z-buffer"
        self.show_faces = False
        self.show_edges = True
        self.fill_opacity = 180
        self.edge_thickness = 1

        self.light_position = [5, 5, -5]
        self.light_enabled = True
        self.lighting_method = "gouraud"
        self.ambient_intensity = 0.3
        self.diffuse_intensity = 0.7
        self.show_light_source = True

        self.previous_states = {
            'faces': {
                'show': True,
                'opacity': 255,
                'edge_thickness': 1
            },
            'edges': {
                'show': True,
                'thickness': 1
            },
            'light': {
                'enabled': True,
                'method': 'flat',
                'ambient': 0.2,
                'diffuse': 0.8,
                'position': [0, 0, 0]
            }
        }

        grid_level = 0
        h = 4  # высота буквы
        y_pos = grid_level + h / 2
        # Буква С слева, повернута на 90 градусов вокруг оси Y
        self.add_letter('С', h, 2, 1, position=[-5, y_pos, 2])
        self.letters[-1].rotation = [0, 90, 0]
        self.letters[-1].update_geometry()
        # Буква Д справа, без поворота
        self.add_letter('Д', h, 2, 1, position=[5, y_pos, 2])
        self.letters[-1].rotation = [0, 0, 0]
        self.letters[-1].update_geometry()

    def add_letter(self, letter, height, width, depth, position=None):
        new_letter = Letter3D(letter, height, width, depth)
        if position:
            new_letter.position = position
        self.letters.append(new_letter)
        if not self.selected_letter:
            self.selected_letter = new_letter

    def project_point(self, point, is_grid=False):
        transformed = point.copy()

        angle_y = math.radians(self.camera_rot[1])
        angle_x = math.radians(self.camera_rot[0])

        x_rot = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z_rot = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x_rot, transformed[1], z_rot]

        y_rot = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z_rot = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y_rot, z_rot]

        f = 500
        z = transformed[2] - self.camera_pos[2]
        if z + f != 0:
            scale_factor = f / (z + f)
            screen_x = transformed[0] * scale_factor * self.scale + self.width() / 2
            screen_y = transformed[1] * scale_factor * self.scale + self.height() / 2
            return QPoint(int(screen_x), int(screen_y))
        return None

    def draw_grid(self, painter):
        grid_color = QColor(80, 80, 80)
        axis_color = QColor(120, 120, 120)

        for i in range(-self.grid_size, self.grid_size + 1):
            for j in range(-self.grid_size, self.grid_size + 1):
                start = [i, 0, j]

                end = [i, 0, j + 1]
                start_view = self.transform_to_view(start)
                end_view = self.transform_to_view(end)
                start_screen = self.project_point(start_view, is_grid=True)
                end_screen = self.project_point(end_view, is_grid=True)
                if start_screen and end_screen:
                    painter.setPen(QPen(axis_color if i == 0 or j == 0 else grid_color, 1))
                    painter.drawLine(start_screen, end_screen)

                end = [i + 1, 0, j]
                end_view = self.transform_to_view(end)
                end_screen = self.project_point(end_view, is_grid=True)
                if start_screen and end_screen:
                    painter.setPen(QPen(axis_color if i == 0 or j == 0 else grid_color, 1))
                    painter.drawLine(start_screen, end_screen)

    def draw_axes(self, painter):
        origin = self.project_point(self.transform_to_view([0, 0, 0]), is_grid=True)
        if origin:
            end = self.project_point(self.transform_to_view([5, 0, 0]), is_grid=True)
            if end:
                painter.setPen(QPen(Qt.red, 2))
                painter.drawLine(origin, end)

            end = self.project_point(self.transform_to_view([0, 5, 0]), is_grid=True)
            if end:
                painter.setPen(QPen(Qt.green, 2))
                painter.drawLine(origin, end)

            end = self.project_point(self.transform_to_view([0, 0, 5]), is_grid=True)
            if end:
                painter.setPen(QPen(Qt.blue, 2))
                painter.drawLine(origin, end)

    def get_face_depth(self, face, letter):
        z_sum = 0
        count = 0

        for vertex in face['vertices']:
            if isinstance(vertex, list):
                local_vertex = vertex
                global_vertex = [
                    local_vertex[0] + letter.position[0],
                    local_vertex[1] + letter.position[1],
                    local_vertex[2] + letter.position[2]
                ]
            else:
                global_vertex = letter.transformed_vertices[vertex]

            angle_y = math.radians(self.camera_rot[1])
            angle_x = math.radians(self.camera_rot[0])

            x_rot = global_vertex[0] * math.cos(angle_y) + global_vertex[2] * math.sin(angle_y)
            z_rot = -global_vertex[0] * math.sin(angle_y) + global_vertex[2] * math.cos(angle_y)

            y_rot = global_vertex[1] * math.cos(angle_x) - z_rot * math.sin(angle_x)
            z_rot = global_vertex[1] * math.sin(angle_x) + z_rot * math.cos(angle_x)

            z_sum += z_rot
            count += 1

        return z_sum / count if count > 0 else 0

    def is_face_visible(self, face, letter):
        normal = face['normal'].copy()

        normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        if normal_length > 0:
            normal = [normal[0] / normal_length, normal[1] / normal_length, normal[2] / normal_length]

        center = [0, 0, 0]
        count = 0

        for vertex in face['vertices']:
            if isinstance(vertex, list):
                center[0] += vertex[0] + letter.position[0]
                center[1] += vertex[1] + letter.position[1]
                center[2] += vertex[2] + letter.position[2]
            else:
                v = letter.transformed_vertices[vertex]
                center[0] += v[0]
                center[1] += v[1]
                center[2] += v[2]
            count += 1

        if count > 0:
            center[0] /= count
            center[1] /= count
            center[2] /= count

        view_dir = [
            self.camera_pos[0] - center[0],
            self.camera_pos[1] - center[1],
            self.camera_pos[2] - center[2]
        ]

        view_length = math.sqrt(view_dir[0] ** 2 + view_dir[1] ** 2 + view_dir[2] ** 2)
        if view_length > 0:
            view_dir = [view_dir[0] / view_length, view_dir[1] / view_length, view_dir[2] / view_length]

        dot_product = normal[0] * view_dir[0] + normal[1] * view_dir[1] + normal[2] * view_dir[2]
        return dot_product > 0

    def paintEvent(self, event):
        self.show_faces = False  # Always only contour
        self.show_edges = True
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(0, 0, 0))

        self.draw_grid(painter)
        self.draw_axes(painter)

        self.draw_z_buffer(painter)

        for letter in self.letters:
            if hasattr(letter, 'show_center') and letter.show_center:
                center_view = self.transform_to_view(letter.transformed_center_point)
                center_point = self.project_point(center_view)
                if center_point:
                    painter.setPen(QPen(Qt.red, 6))
                    painter.setBrush(QColor(255, 0, 0))
                    painter.drawEllipse(center_point, 3, 3)

        if self.show_light_source and self.light_enabled:
            light_screen_pos = self.project_point(self.light_position)
            if light_screen_pos:
                painter.setPen(QPen(Qt.yellow, 8))
                painter.setBrush(QColor(255, 255, 0))
                painter.drawEllipse(light_screen_pos, 5, 5)

    def draw_z_buffer(self, painter):
        width = self.width()
        height = self.height()

        z_buffer = [[float('-inf') for _ in range(width)] for _ in range(height)]
        color_buffer = [[None for _ in range(width)] for _ in range(height)]

        # Do not draw colored face contours at all
        # Only draw all edges (wireframe) in white
        for letter in self.letters:
            color = [255, 255, 255]  # White wireframe
            for edge in letter.edges:
                v1 = letter.transformed_vertices[edge[0]]
                v2 = letter.transformed_vertices[edge[1]]
                v1_view = self.transform_to_view(v1)
                v2_view = self.transform_to_view(v2)
                p1, z1 = self.project_point_with_z(v1_view)
                p2, z2 = self.project_point_with_z(v2_view)
                if p1 and p2:
                    self.draw_line_with_z_buffer(p1.x(), p1.y(), p2.x(), p2.y(), z1, z2, color, z_buffer, color_buffer)

        for y in range(height):
            for x in range(width):
                color_info = color_buffer[y][x]
                if color_info:
                    color = color_info['color']
                    is_edge = color_info['is_edge']

                    if is_edge:
                        painter.setPen(QColor(color[0], color[1], color[2], 255))
                        painter.drawPoint(x, y)

    def project_point_with_z(self, point):
        transformed = point.copy()

        angle_y = math.radians(self.camera_rot[1])
        angle_x = math.radians(self.camera_rot[0])

        x_rot = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z_rot = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x_rot, transformed[1], z_rot]

        y_rot = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z_rot = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y_rot, z_rot]

        z_value = transformed[2] - self.camera_pos[2]

        f = 500
        z = transformed[2] - self.camera_pos[2]
        if z + f != 0:
            scale_factor = f / (z + f)
            screen_x = transformed[0] * scale_factor * self.scale + self.width() / 2
            screen_y = transformed[1] * scale_factor * self.scale + self.height() / 2
            return QPoint(int(screen_x), int(screen_y)), z_value
        return None, 0

    def rasterize_face_with_z_buffer(self, screen_vertices, z_values, color, z_buffer, color_buffer):
        num_vertices = len(screen_vertices)

        for i in range(1, num_vertices - 1):
            triangle = [screen_vertices[0], screen_vertices[i], screen_vertices[i + 1]]
            triangle_z = [z_values[0], z_values[i], z_values[i + 1]]
            self.rasterize_triangle_with_z_buffer(triangle, triangle_z, color, z_buffer, color_buffer)

        if self.show_edges:
            for i in range(num_vertices):
                p1 = screen_vertices[i]
                p2 = screen_vertices[(i + 1) % num_vertices]
                z1 = z_values[i]
                z2 = z_values[(i + 1) % num_vertices]
                self.draw_line_with_z_buffer(p1.x(), p1.y(), p2.x(), p2.y(), z1, z2, color, z_buffer, color_buffer)

    def draw_line_with_z_buffer(self, x0, y0, x1, y1, z0, z1, color, z_buffer, color_buffer):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx, dy = dy, dx

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            z0, z1 = z1, z0

        dx = x1 - x0
        dy = abs(y1 - y0)
        error = dx // 2
        y = y0
        y_step = 1 if y0 < y1 else -1

        width = len(z_buffer[0])
        height = len(z_buffer)

        for x in range(x0, x1 + 1):
            t = (x - x0) / max(1, float(x1 - x0))
            z = z0 * (1 - t) + z1 * t

            coord_x, coord_y = (y, x) if steep else (x, y)

            if 0 <= coord_x < width and 0 <= coord_y < height:
                if z > z_buffer[coord_y][coord_x]:
                    z_buffer[coord_y][coord_x] = z
                    color_buffer[coord_y][coord_x] = {
                        'color': color,
                        'is_edge': True
                    }

            error -= dy
            if error < 0:
                y += y_step
                error += dx

    def rasterize_triangle_with_z_buffer(self, triangle_screen, triangle_z, color, z_buffer, color_buffer):
        min_x = max(0, min(triangle_screen[0].x(), triangle_screen[1].x(), triangle_screen[2].x()))
        max_x = min(len(z_buffer[0]) - 1, max(triangle_screen[0].x(), triangle_screen[1].x(), triangle_screen[2].x()))
        min_y = max(0, min(triangle_screen[0].y(), triangle_screen[1].y(), triangle_screen[2].y()))
        max_y = min(len(z_buffer) - 1, max(triangle_screen[0].y(), triangle_screen[1].y(), triangle_screen[2].y()))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if self.is_point_in_triangle(x, y, triangle_screen):
                    barycentric = self.get_barycentric_coords(
                        x, y,
                        triangle_screen[0].x(), triangle_screen[0].y(),
                        triangle_screen[1].x(), triangle_screen[1].y(),
                        triangle_screen[2].x(), triangle_screen[2].y()
                    )

                    if barycentric:
                        z = (
                                barycentric[0] * triangle_z[0] +
                                barycentric[1] * triangle_z[1] +
                                barycentric[2] * triangle_z[2]
                        )

                        if z > z_buffer[y][x]:
                            z_buffer[y][x] = z
                            color_buffer[y][x] = {
                                'color': color,
                                'is_edge': False
                            }

    def transform_to_view(self, point):
        transformed = point.copy()

        angle_y = math.radians(self.camera_rot[1])
        angle_x = math.radians(self.camera_rot[0])

        x_rot = transformed[0] * math.cos(angle_y) + transformed[2] * math.sin(angle_y)
        z_rot = -transformed[0] * math.sin(angle_y) + transformed[2] * math.cos(angle_y)
        transformed = [x_rot, transformed[1], z_rot]

        y_rot = transformed[1] * math.cos(angle_x) - transformed[2] * math.sin(angle_x)
        z_rot = transformed[1] * math.sin(angle_x) + transformed[2] * math.cos(angle_x)
        transformed = [transformed[0], y_rot, z_rot]

        return transformed

    def is_point_in_triangle(self, x, y, triangle):
        def sign(p1, p2, p3):
            return (p1.x() - p3.x()) * (p2.y() - p3.y()) - (p2.x() - p3.x()) * (p1.y() - p3.y())

        pt = QPoint(x, y)
        d1 = sign(pt, triangle[0], triangle[1])
        d2 = sign(pt, triangle[1], triangle[2])
        d3 = sign(pt, triangle[2], triangle[0])

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get_barycentric_coords(self, x, y, x1, y1, x2, y2, x3, y3):
        det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)

        if abs(det) < 1e-6:
            return None

        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
        gamma = 1 - alpha - beta

        if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
            return [alpha, beta, gamma]

        return None

    def get_face_color(self, face, letter):
        if letter.letter == 'С':
            base_color = [100, 100, 255]
        else:
            base_color = [255, 100, 100]

        if not self.light_enabled:
            return base_color

        normal = face['normal'].copy()

        normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        if normal_length > 0:
            normal = [normal[0] / normal_length, normal[1] / normal_length, normal[2] / normal_length]

        center = [0, 0, 0]
        count = 0

        for vertex in face['vertices']:
            if isinstance(vertex, list):
                center[0] += vertex[0] + letter.position[0]
                center[1] += vertex[1] + letter.position[1]
                center[2] += vertex[2] + letter.position[2]
            else:
                v = letter.transformed_vertices[vertex]
                center[0] += v[0]
                center[1] += v[1]
                center[2] += v[2]
            count += 1

        if count > 0:
            center[0] /= count
            center[1] /= count
            center[2] /= count

        light_dir = [
            self.light_position[0] - center[0],
            self.light_position[1] - center[1],
            self.light_position[2] - center[2]
        ]

        light_length = math.sqrt(light_dir[0] ** 2 + light_dir[1] ** 2 + light_dir[2] ** 2)
        if light_length > 0:
            light_dir = [light_dir[0] / light_length, light_dir[1] / light_length, light_dir[2] / light_length]

        dot_product = max(0, normal[0] * light_dir[0] + normal[1] * light_dir[1] + normal[2] * light_dir[2])

        if self.lighting_method == "flat":
            light_factor = self.ambient_intensity + self.diffuse_intensity * dot_product
        elif self.lighting_method == "gouraud":
            light_factor = self.ambient_intensity + self.diffuse_intensity * dot_product
        elif self.lighting_method == "phong":
            light_factor = self.ambient_intensity + self.diffuse_intensity * dot_product
        else:
            light_factor = self.ambient_intensity + self.diffuse_intensity * dot_product

        color = [
            min(255, int(base_color[0] * light_factor)),
            min(255, int(base_color[1] * light_factor)),
            min(255, int(base_color[2] * light_factor))
        ]

        return color

    def mousePressEvent(self, event):
        self.last_pos = QPoint(int(event.position().x()), int(event.position().y()))
        self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if not self.mouse_pressed:
            return

        current_pos = QPoint(int(event.position().x()), int(event.position().y()))
        dx = current_pos.x() - self.last_pos.x()
        dy = current_pos.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.camera_rot[1] += dx * 0.5
            self.camera_rot[0] += dy * 0.5
        elif event.buttons() & Qt.RightButton:
            if self.selected_letter:
                if event.modifiers() & Qt.ShiftModifier:
                    self.selected_letter.position[1] += dy * 0.1
                elif event.modifiers() & Qt.ControlModifier:
                    self.selected_letter.position[2] -= dy * 0.1
                else:
                    self.selected_letter.position[0] += dx * 0.1
                self.selected_letter.update_geometry()

        self.last_pos = current_pos
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.scale *= pow(1.001, delta)
        self.update()

    def move_selected(self, axis, direction):
        if self.selected_letter:
            step = direction * self.movement_step
            if axis == 'x':
                self.selected_letter.position[0] += step
            elif axis == 'y':
                self.selected_letter.position[1] += step
            elif axis == 'z':
                self.selected_letter.position[2] += step
            self.selected_letter.update_geometry()
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
            factor = 1.1 if direction > 0 else 1 / 1.1
            self.selected_letter.scale_object(axis, factor)
            self.update()

    def set_rotation_step(self, value):
        self.rotation_step = value

    def set_uniform_scale(self, scale):
        if self.selected_letter:
            self.selected_letter.set_uniform_scale(scale)
            self.update()

    def set_render_mode(self, mode):
        self.render_mode = mode
        self.update()

    def toggle_faces(self, state):
        if state == Qt.Checked:
            # Restore previous state
            self.show_faces = self.previous_states['faces']['show']
            self.fill_opacity = self.previous_states['faces']['opacity']
            self.edge_thickness = self.previous_states['faces']['edge_thickness']
        else:
            # Store current state
            self.previous_states['faces'] = {
                'show': self.show_faces,
                'opacity': self.fill_opacity,
                'edge_thickness': self.edge_thickness
            }
            # Clear current state
            self.show_faces = False
            self.fill_opacity = 0
            self.edge_thickness = 0
        self.update()

    def toggle_edges(self, state):
        if state == Qt.Checked:
            # Restore previous state
            self.show_edges = self.previous_states['edges']['show']
            self.edge_thickness = self.previous_states['edges']['thickness']
        else:
            # Store current state
            self.previous_states['edges'] = {
                'show': self.show_edges,
                'thickness': self.edge_thickness
            }
            # Clear current state
            self.show_edges = False
            self.edge_thickness = 0
        self.update()

    def set_fill_opacity(self, opacity):
        self.fill_opacity = opacity
        self.update()

    def set_edge_thickness(self, thickness):
        self.edge_thickness = thickness
        self.update()

    def move_light(self, axis, direction):
        step = direction * self.movement_step
        if axis == 'x':
            self.light_position[0] += step
        elif axis == 'y':
            self.light_position[1] += step
        elif axis == 'z':
            self.light_position[2] += step
        self.update()

    def toggle_light(self, state):
        if state == Qt.Checked:
            # Restore previous state
            self.light_enabled = self.previous_states['light']['enabled']
            self.lighting_method = self.previous_states['light']['method']
            self.ambient_intensity = self.previous_states['light']['ambient']
            self.diffuse_intensity = self.previous_states['light']['diffuse']
            self.light_position = self.previous_states['light']['position'].copy()
        else:
            # Store current state
            self.previous_states['light'] = {
                'enabled': self.light_enabled,
                'method': self.lighting_method,
                'ambient': self.ambient_intensity,
                'diffuse': self.diffuse_intensity,
                'position': self.light_position.copy()
            }
            # Clear current state
            self.light_enabled = False
            self.lighting_method = 'flat'
            self.ambient_intensity = 0.0
            self.diffuse_intensity = 0.0
            self.light_position = [0, 0, 0]
        self.update()

    def set_lighting_method(self, method):
        self.lighting_method = method
        self.update()

    def set_ambient_intensity(self, intensity):
        self.ambient_intensity = intensity
        self.update()

    def set_diffuse_intensity(self, intensity):
        self.diffuse_intensity = intensity
        self.update()

    def toggle_light_source_visibility(self, state):
        self.show_light_source = state == Qt.Checked
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Viewer")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        self.viewer = ViewerWidget()
        main_layout.addWidget(self.viewer, stretch=3)

        control_scroll = QScrollArea()
        control_scroll.setWidgetResizable(True)
        control_scroll.setMinimumWidth(300)

        control_panel = QWidget()
        control_scroll.setWidget(control_panel)
        main_layout.addWidget(control_scroll, stretch=1)

        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(5)

        tab_widget = QTabWidget()
        control_layout.addWidget(tab_widget)

        letter_tab = QWidget()
        letter_layout = QVBoxLayout(letter_tab)
        letter_layout.setSpacing(5)

        letter_selector_group = QGroupBox("Выбор буквы")
        letter_selector_layout = QVBoxLayout(letter_selector_group)
        letter_selector_layout.setContentsMargins(5, 10, 5, 5)
        self.letter_combo = QComboBox()
        self.letter_combo.addItems(["Буква С", "Буква Д"])
        self.letter_combo.currentIndexChanged.connect(self.change_selected_letter)
        letter_selector_layout.addWidget(self.letter_combo)
        letter_layout.addWidget(letter_selector_group)

        self.letter_params_group = QGroupBox("Параметры букв")
        letter_params_layout = QVBoxLayout(self.letter_params_group)
        letter_params_layout.setContentsMargins(5, 10, 5, 5)

        self.c_params_widget = QWidget()
        c_params_layout = QVBoxLayout(self.c_params_widget)
        c_params_layout.setContentsMargins(0, 0, 0, 0)
        c_params_layout.setSpacing(3)

        c_height_layout = QHBoxLayout()
        c_height_layout.addWidget(QLabel("Высота:"))
        self.c_height_spin = QDoubleSpinBox()
        self.c_height_spin.setRange(0.1, 20.0)
        self.c_height_spin.setValue(4.0)
        self.c_height_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_height_layout.addWidget(self.c_height_spin)
        c_params_layout.addLayout(c_height_layout)

        c_width_layout = QHBoxLayout()
        c_width_layout.addWidget(QLabel("Ширина:"))
        self.c_width_spin = QDoubleSpinBox()
        self.c_width_spin.setRange(0.1, 20.0)
        self.c_width_spin.setValue(2.0)
        self.c_width_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_width_layout.addWidget(self.c_width_spin)
        c_params_layout.addLayout(c_width_layout)

        c_depth_layout = QHBoxLayout()
        c_depth_layout.addWidget(QLabel("Глубина:"))
        self.c_depth_spin = QDoubleSpinBox()
        self.c_depth_spin.setRange(0.1, 20.0)
        self.c_depth_spin.setValue(1.0)
        self.c_depth_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_depth_layout.addWidget(self.c_depth_spin)
        c_params_layout.addLayout(c_depth_layout)

        self.d_params_widget = QWidget()
        d_params_layout = QVBoxLayout(self.d_params_widget)
        d_params_layout.setContentsMargins(0, 0, 0, 0)
        d_params_layout.setSpacing(3)

        d_height_layout = QHBoxLayout()
        d_height_layout.addWidget(QLabel("Высота:"))
        self.d_height_spin = QDoubleSpinBox()
        self.d_height_spin.setRange(0.1, 20.0)
        self.d_height_spin.setValue(4.0)
        self.d_height_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_height_layout.addWidget(self.d_height_spin)
        d_params_layout.addLayout(d_height_layout)

        d_width_layout = QHBoxLayout()
        d_width_layout.addWidget(QLabel("Ширина:"))
        self.d_width_spin = QDoubleSpinBox()
        self.d_width_spin.setRange(0.1, 20.0)
        self.d_width_spin.setValue(2.0)
        self.d_width_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_width_layout.addWidget(self.d_width_spin)
        d_params_layout.addLayout(d_width_layout)

        d_depth_layout = QHBoxLayout()
        d_depth_layout.addWidget(QLabel("Глубина:"))
        self.d_depth_spin = QDoubleSpinBox()
        self.d_depth_spin.setRange(0.1, 20.0)
        self.d_depth_spin.setValue(1.0)
        self.d_depth_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_depth_layout.addWidget(self.d_depth_spin)
        d_params_layout.addLayout(d_depth_layout)

        letter_params_layout.addWidget(self.c_params_widget)
        letter_params_layout.addWidget(self.d_params_widget)

        self.d_params_widget.hide()

        letter_layout.addWidget(self.letter_params_group)
        tab_widget.addTab(letter_tab, "Буква")

        transform_tab = QWidget()
        transform_layout = QVBoxLayout(transform_tab)
        transform_layout.setSpacing(5)

        movement_group = QGroupBox("Перемещение")
        movement_layout = QVBoxLayout(movement_group)
        movement_layout.setContentsMargins(5, 10, 5, 5)
        movement_layout.setSpacing(3)

        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel("Шаг:"))
        step_spin = QDoubleSpinBox()
        step_spin.setRange(0.1, 5.0)
        step_spin.setValue(0.5)
        step_spin.setSingleStep(0.1)
        step_spin.valueChanged.connect(self.update_movement_step)
        step_layout.addWidget(step_spin)
        movement_layout.addLayout(step_layout)

        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X:"))
        x_minus = QPushButton("-X")
        x_minus.clicked.connect(lambda: self.viewer.move_selected('x', -1))
        x_plus = QPushButton("+X")
        x_plus.clicked.connect(lambda: self.viewer.move_selected('x', 1))
        x_layout.addWidget(x_minus)
        x_layout.addWidget(x_plus)
        movement_layout.addLayout(x_layout)

        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y:"))
        y_minus = QPushButton("-Y")
        y_minus.clicked.connect(lambda: self.viewer.move_selected('y', -1))
        y_plus = QPushButton("+Y")
        y_plus.clicked.connect(lambda: self.viewer.move_selected('y', 1))
        y_layout.addWidget(y_minus)
        y_layout.addWidget(y_plus)
        movement_layout.addLayout(y_layout)

        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Z:"))
        z_minus = QPushButton("-Z")
        z_minus.clicked.connect(lambda: self.viewer.move_selected('z', -1))
        z_plus = QPushButton("+Z")
        z_plus.clicked.connect(lambda: self.viewer.move_selected('z', 1))
        z_layout.addWidget(z_minus)
        z_layout.addWidget(z_plus)
        movement_layout.addLayout(z_layout)

        transform_layout.addWidget(movement_group)

        rotation_group = QGroupBox("Вращение")
        rotation_layout = QVBoxLayout(rotation_group)
        rotation_layout.setContentsMargins(5, 10, 5, 5)

        rotation_step_layout = QHBoxLayout()
        rotation_step_layout.addWidget(QLabel("Шаг:"))
        rotation_step_spin = QSpinBox()
        rotation_step_spin.setRange(1, 90)
        rotation_step_spin.setValue(5)
        rotation_step_spin.valueChanged.connect(self.update_rotation_step)
        rotation_step_layout.addWidget(rotation_step_spin)
        rotation_layout.addLayout(rotation_step_layout)

        x_rot_layout = QHBoxLayout()
        x_rot_layout.addWidget(QLabel("X:"))
        x_rot_minus = QPushButton("-X")
        x_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('x', -1))
        x_rot_plus = QPushButton("+X")
        x_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('x', 1))
        x_rot_layout.addWidget(x_rot_minus)
        x_rot_layout.addWidget(x_rot_plus)
        rotation_layout.addLayout(x_rot_layout)

        y_rot_layout = QHBoxLayout()
        y_rot_layout.addWidget(QLabel("Y:"))
        y_rot_minus = QPushButton("-Y")
        y_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('y', -1))
        y_rot_plus = QPushButton("+Y")
        y_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('y', 1))
        y_rot_layout.addWidget(y_rot_minus)
        y_rot_layout.addWidget(y_rot_plus)
        rotation_layout.addLayout(y_rot_layout)

        z_rot_layout = QHBoxLayout()
        z_rot_layout.addWidget(QLabel("Z:"))
        z_rot_minus = QPushButton("-Z")
        z_rot_minus.clicked.connect(lambda: self.viewer.rotate_selected('z', -1))
        z_rot_plus = QPushButton("+Z")
        z_rot_plus.clicked.connect(lambda: self.viewer.rotate_selected('z', 1))
        z_rot_layout.addWidget(z_rot_minus)
        z_rot_layout.addWidget(z_rot_plus)
        rotation_layout.addLayout(z_rot_layout)

        transform_layout.addWidget(rotation_group)

        scale_group = QGroupBox("Масштаб")
        scale_layout = QVBoxLayout(scale_group)
        scale_layout.setContentsMargins(5, 10, 5, 5)

        scale_layout.addWidget(QLabel("Масштаб:"))
        scale_spin = QDoubleSpinBox()
        scale_spin.setRange(0.1, 10.0)
        scale_spin.setValue(1.0)
        scale_spin.setSingleStep(0.1)
        scale_spin.valueChanged.connect(lambda v: self.viewer.set_uniform_scale(v))
        scale_layout.addWidget(scale_spin)

        transform_layout.addWidget(scale_group)

        reflection_group = QGroupBox("Отражение")
        reflection_layout = QVBoxLayout(reflection_group)
        reflection_layout.setContentsMargins(5, 10, 5, 5)

        x_reflect = QPushButton("Отражение по X")
        x_reflect.clicked.connect(lambda: self.viewer.reflect_selected('x'))
        reflection_layout.addWidget(x_reflect)

        y_reflect = QPushButton("Отражение по Y")
        y_reflect.clicked.connect(lambda: self.viewer.reflect_selected('y'))
        reflection_layout.addWidget(y_reflect)

        z_reflect = QPushButton("Отражение по Z")
        z_reflect.clicked.connect(lambda: self.viewer.reflect_selected('z'))
        reflection_layout.addWidget(z_reflect)

        transform_layout.addWidget(reflection_group)
        tab_widget.addTab(transform_tab, "Трансформации")

        help_text = QLabel(
            "Управление:\n"
            "ЛКМ - вращение камеры\n"
            "ПКМ - перемещение по X\n"
            "ПКМ + Shift - перемещение по Y\n"
            "ПКМ + Ctrl - перемещение по Z\n"
            "Колесико - масштаб просмотра"
        )
        control_layout.addWidget(help_text)

        self.step_spin = step_spin
        self.rotation_step_spin = rotation_step_spin
        self.scale_spin = scale_spin

        self.change_selected_letter(0)

    def change_selected_letter(self, index):
        if index == 0:
            self.viewer.selected_letter = self.viewer.letters[0]
            self.c_params_widget.show()
            self.d_params_widget.hide()
        else:
            self.viewer.selected_letter = self.viewer.letters[1]
            self.c_params_widget.hide()
            self.d_params_widget.show()
        self.viewer.update()

    def update_letter_params(self, letter):
        if letter == "С" and self.viewer.letters[0]:
            self.viewer.letters[0].height = self.c_height_spin.value()
            self.viewer.letters[0].width = self.c_width_spin.value()
            self.viewer.letters[0].depth = self.c_depth_spin.value()
            self.viewer.letters[0].update_geometry()
        elif letter == "Д" and self.viewer.letters[1]:
            self.viewer.letters[1].height = self.d_height_spin.value()
            self.viewer.letters[1].width = self.d_width_spin.value()
            self.viewer.letters[1].depth = self.d_depth_spin.value()
            self.viewer.letters[1].update_geometry()
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
        self.center_point = [0, 0, 0]  # Точка центра буквы в локальных координатах
        self.transformed_center_point = [0, 0, 0]  # Точка центра в глобальных координатах
        self.show_center = True  # Показывать или нет точку центра
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
        if self.letter == 'С':
            self.create_letter_c()
        elif self.letter == 'Д':
            self.create_letter_de()
        
        # Вычисляем точку центра буквы (относительные координаты)
        self.calculate_center_point()
        
        # После создания геометрии обновляем трансформированные вершины
        self.transformed_vertices = [self.transform_vertex(v) for v in self.vertices]
        # Обновляем трансформированную точку центра
        self.transformed_center_point = self.transform_vertex(self.center_point)
    
    def calculate_center_point(self):
        """Вычисляет точку центра буквы в локальных координатах"""
        if self.letter == 'С':
            # Для буквы С центр смещаем внутрь полукруга
            self.center_point = [self.width * 0.6, self.height * 0.5, self.depth / 2]
        elif self.letter == 'Д':
            # Для буквы Д центр смещаем внутрь центральной части
            self.center_point = [self.width / 2, self.height * 0.4, self.depth / 2]
    
    def toggle_center_point(self):
        """Включает/выключает отображение точки центра"""
        self.show_center = not self.show_center
        return self.show_center
    
    def create_letter_c(self):
        """Создает букву C (кириллическая С)"""
        self.vertices = []
        self.edges = []
        self.faces = []
        
        h = self.height
        w = self.width
        d = self.depth
        t = w * 0.15  # толщина стенки
        
        # Улучшенная версия русской буквы С
        segments = 14  # увеличиваем число сегментов для более гладкой формы
        
        # Внешний контур - передняя часть
        front_outer = []
        for i in range(segments+1):
            # Используем дугу 220 градусов вместо 180 для более закругленной С
            angle = math.radians(110) - math.radians(220) * i / segments
            # Смещаем центр дуги для более естественной формы
            x = w * 0.6 + w * 0.4 * math.cos(angle)
            y = h * 0.5 + h * 0.5 * math.sin(angle)
            front_outer.append([x, y, 0])
        
        # Внутренний контур - передняя часть
        front_inner = []
        for i in range(segments+1):
            angle = math.radians(110) - math.radians(220) * i / segments
            # Уменьшаем радиус для внутреннего контура
            x = w * 0.6 + (w * 0.4 - t) * math.cos(angle)
            y = h * 0.5 + (h * 0.5 - t) * math.sin(angle)
            front_inner.append([x, y, 0])
        
        # Создаем заднюю часть
        back_outer = [[v[0], v[1], v[2] + d] for v in front_outer]
        back_inner = [[v[0], v[1], v[2] + d] for v in front_inner]
        
        # Сохраняем вершины
        self.vertices = front_outer + front_inner + back_outer + back_inner
        
        # Соединяем вершины ребрами
        def add_edge(v1, v2):
            edge = (min(v1, v2), max(v1, v2))
            if edge not in self.edges:
                self.edges.append(edge)
        
        # Соединяем внешний контур спереди
        for i in range(len(front_outer) - 1):
            add_edge(i, i + 1)
        
        # Соединяем внутренний контур спереди
        inner_offset = len(front_outer)
        for i in range(len(front_inner) - 1):
            add_edge(inner_offset + i, inner_offset + i + 1)
        
        # Соединяем внешний контур сзади
        back_offset = inner_offset + len(front_inner)
        for i in range(len(back_outer) - 1):
            add_edge(back_offset + i, back_offset + i + 1)
        
        # Соединяем внутренний контур сзади
        back_inner_offset = back_offset + len(back_outer)
        for i in range(len(back_inner) - 1):
            add_edge(back_inner_offset + i, back_inner_offset + i + 1)
        
        # Соединяем переднюю и заднюю части
        # Соединяем верхний и нижний края
        add_edge(0, back_offset)  # верхний край внешний
        add_edge(len(front_outer) - 1, back_offset + len(back_outer) - 1)  # нижний край внешний
        add_edge(inner_offset, back_inner_offset)  # верхний край внутренний
        add_edge(inner_offset + len(front_inner) - 1, back_inner_offset + len(back_inner) - 1)  # нижний край внутренний
        
        # Добавляем соединения между внешним и внутренним контурами на краях
        add_edge(0, inner_offset)  # верхний край спереди
        add_edge(len(front_outer) - 1, inner_offset + len(front_inner) - 1)  # нижний край спереди
        add_edge(back_offset, back_inner_offset)  # верхний край сзади
        add_edge(back_offset + len(back_outer) - 1, back_inner_offset + len(back_inner) - 1)  # нижний край сзади
        
        # Добавляем дополнительные соединения между внешним и внутренним контурами
        # Выбираем несколько ключевых точек для соединения, чтобы не перегружать модель
        connection_points = [segments // 4, segments // 2, 3 * segments // 4]
        
        for i in connection_points:
            # Соединяем точки на передней грани
            add_edge(i, inner_offset + i)
            # Соединяем точки на задней грани
            add_edge(back_offset + i, back_inner_offset + i)
            
            # Дополнительно соединяем соответствующие точки на передней и задней гранях
            # для создания "перегородок" внутри буквы
            add_edge(i, back_offset + i)
            add_edge(inner_offset + i, back_inner_offset + i)
            
        # Добавляем грани
        self.faces = [
            # Передние грани
            {'vertices': front_outer, 'normal': [0, 0, -1]},
            {'vertices': front_inner, 'normal': [0, 0, 1]},
            
            # Задние грани
            {'vertices': [v for v in reversed(back_outer)], 'normal': [0, 0, 1]},
            {'vertices': [v for v in reversed(back_inner)], 'normal': [0, 0, -1]},
            
            # Боковые грани (верхняя и нижняя)
            {'vertices': [front_outer[0], front_inner[0], back_inner[0], back_outer[0]], 
             'normal': [0, 1, 0]},  # верхняя грань
            {'vertices': [front_outer[-1], front_inner[-1], back_inner[-1], back_outer[-1]], 
             'normal': [0, -1, 0]},  # нижняя грань
        ]
        
        # Добавляем "перегородки" в качестве граней для лучшей визуализации
        for i in connection_points:
            # Добавляем перегородку
            self.faces.append({
                'vertices': [
                    front_outer[i], 
                    front_inner[i], 
                    back_inner[i],
                    back_outer[i]
                ],
                'normal': [math.sin(math.radians(110) - math.radians(220) * i / segments), 
                          -math.cos(math.radians(110) - math.radians(220) * i / segments), 
                          0]
            })

    def create_letter_de(self):
        """Создает букву Д (кириллическая Д)"""
        self.vertices = []
        self.edges = []
        self.faces = []
        
        h = self.height
        w = self.width
        d = self.depth
        leg_h = h * 0.15  # высота ножек
        leg_w = w * 0.1   # ширина выступа ножек
        t = w * 0.15      # толщина стенок
        
        # Основные точки буквы Д (передняя часть)
        
        # Основной прямоугольник с ножками (внешний контур)
        front_outer = [
            [-leg_w, -leg_h, 0],        # низ левой ножки 
            [w + leg_w, -leg_h, 0],     # низ правой ножки
            [w + leg_w, 0, 0],          # низ правой стенки
            [w, 0, 0],                  # внутренний низ правой стенки
            [w, h - t, 0],              # верх правой стенки
            [0, h - t, 0],              # верх левой стенки
            [0, 0, 0],                  # внутренний низ левой стенки
            [-leg_w, 0, 0]              # низ левой стенки
        ]
        
        # Верхняя перекладина (крыша)
        front_roof = [
            [0, h - t, 0],              # левый край крыши
            [w, h - t, 0],              # правый край крыши
            [w - t, h, 0],              # правый верхний угол
            [t, h, 0]                   # левый верхний угол
        ]
        
        # Внутренний прямоугольник (полость)
        front_inner = [
            [t, t, 0],                  # нижний левый
            [w - t, t, 0],              # нижний правый
            [w - t, h - t * 2, 0],      # верхний правый
            [t, h - t * 2, 0]           # верхний левый
        ]
        
        # Задние контуры
        back_outer = [[v[0], v[1], v[2] + d] for v in front_outer]
        back_roof = [[v[0], v[1], v[2] + d] for v in front_roof]
        back_inner = [[v[0], v[1], v[2] + d] for v in front_inner]
        
        # Сохраняем вершины
        self.vertices = front_outer + front_roof + front_inner + back_outer + back_roof + back_inner
        
        # Функция для добавления ребра
        def add_edge(v1_idx, v2_idx):
            edge = (min(v1_idx, v2_idx), max(v1_idx, v2_idx))
            if edge not in self.edges:
                self.edges.append(edge)
                
        # Соединяем внешний контур (передний)
        for i in range(len(front_outer)):
            add_edge(i, (i + 1) % len(front_outer))
            
        # Соединяем крышу (передняя)
        roof_offset = len(front_outer)
        for i in range(len(front_roof)):
            add_edge(roof_offset + i, roof_offset + (i + 1) % len(front_roof))
            
        # Соединяем внутренний контур (передний)
        inner_offset = roof_offset + len(front_roof)
        for i in range(len(front_inner)):
            add_edge(inner_offset + i, inner_offset + (i + 1) % len(front_inner))
            
        # Соединяем внешний контур (задний)
        back_offset = inner_offset + len(front_inner)
        for i in range(len(back_outer)):
            add_edge(back_offset + i, back_offset + (i + 1) % len(back_outer))
            
        # Соединяем крышу (задняя)
        back_roof_offset = back_offset + len(back_outer)
        for i in range(len(back_roof)):
            add_edge(back_roof_offset + i, back_roof_offset + (i + 1) % len(back_roof))
            
        # Соединяем внутренний контур (задний)
        back_inner_offset = back_roof_offset + len(back_roof)
        for i in range(len(back_inner)):
            add_edge(back_inner_offset + i, back_inner_offset + (i + 1) % len(back_inner))
            
        # Соединяем переднюю и заднюю части
        # Внешний контур
        for i in range(len(front_outer)):
            add_edge(i, back_offset + i)
            
        # Крыша
        for i in range(len(front_roof)):
            add_edge(roof_offset + i, back_roof_offset + i)
            
        # Внутренний контур
        for i in range(len(front_inner)):
            add_edge(inner_offset + i, back_inner_offset + i)
            
        # Соединяем крышу с основным контуром
        add_edge(5, roof_offset)        # левый угол
        add_edge(4, roof_offset + 1)    # правый угол
        add_edge(back_offset + 5, back_roof_offset)     # левый задний угол
        add_edge(back_offset + 4, back_roof_offset + 1) # правый задний угол
        
        # Добавляем грани
        self.faces = [
            # Передние грани
            {'vertices': front_outer, 'normal': [0, 0, -1]},
            {'vertices': front_roof, 'normal': [0, 0, -1]},
            {'vertices': front_inner, 'normal': [0, 0, 1]},
            
            # Задние грани
            {'vertices': back_outer, 'normal': [0, 0, 1]},
            {'vertices': back_roof, 'normal': [0, 0, 1]},
            {'vertices': back_inner, 'normal': [0, 0, -1]},
        ]

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
        
        # Настройки для второго этапа:
        self.render_mode = "z-buffer"  # Режим рендеринга: "wireframe", "depth-sort", "z-buffer"
        self.show_faces = True  # Показывать заливку граней
        self.show_edges = True  # Показывать рёбра
        self.fill_opacity = 180  # Непрозрачность заливки (0-255)
        self.edge_thickness = 1  # Толщина рёбер в пикселях
        
        # Добавляем буквы
        self.add_letter('С', 4, 2, 1, position=[-3, 0, 0])
        self.add_letter('Д', 4, 2, 1, position=[3, 0, 0])
    
    def add_letter(self, letter, height, width, depth, position=None):
        new_letter = Letter3D(letter, height, width, depth)
        if position:
            new_letter.position = position
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
        count = 0
        
        for vertex in face['vertices']:
            if isinstance(vertex, list):
                # Это локальные координаты
                local_vertex = vertex
                global_vertex = [
                    local_vertex[0] + letter.position[0],
                    local_vertex[1] + letter.position[1],
                    local_vertex[2] + letter.position[2]
                ]
            else:
                # Это индекс вершины в списке transformed_vertices
                global_vertex = letter.transformed_vertices[vertex]
            
            # Поворот камеры
            angle_y = math.radians(self.camera_rot[1])
            angle_x = math.radians(self.camera_rot[0])
            
            # Поворот вокруг Y
            x_rot = global_vertex[0] * math.cos(angle_y) + global_vertex[2] * math.sin(angle_y)
            z_rot = -global_vertex[0] * math.sin(angle_y) + global_vertex[2] * math.cos(angle_y)
            
            # Поворот вокруг X
            y_rot = global_vertex[1] * math.cos(angle_x) - z_rot * math.sin(angle_x)
            z_rot = global_vertex[1] * math.sin(angle_x) + z_rot * math.cos(angle_x)
            
            z_sum += z_rot
            count += 1
        
        return z_sum / count if count > 0 else 0

    def is_face_visible(self, face, letter):
        """Проверяет видимость грани в зависимости от её нормали и положения камеры"""
        # Вычисляем нормаль грани в мировых координатах
        normal = face['normal'].copy()
        
        # Нормализуем нормаль (убедимся, что длина = 1)
        normal_length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if normal_length > 0:
            normal = [normal[0]/normal_length, normal[1]/normal_length, normal[2]/normal_length]
        
        # Вычисляем центр грани
        center = [0, 0, 0]
        count = 0
        
        for vertex in face['vertices']:
            if isinstance(vertex, list):
                # Это локальные координаты
                center[0] += vertex[0] + letter.position[0]
                center[1] += vertex[1] + letter.position[1]
                center[2] += vertex[2] + letter.position[2]
            else:
                # Это индекс вершины в списке transformed_vertices
                v = letter.transformed_vertices[vertex]
                center[0] += v[0]
                center[1] += v[1]
                center[2] += v[2]
            count += 1
            
        if count > 0:
            center[0] /= count
            center[1] /= count
            center[2] /= count
        
        # Вычисляем вектор от центра грани к камере
        view_dir = [
            self.camera_pos[0] - center[0], 
            self.camera_pos[1] - center[1], 
            self.camera_pos[2] - center[2]
        ]
        
        # Нормализуем вектор направления взгляда
        view_length = math.sqrt(view_dir[0]**2 + view_dir[1]**2 + view_dir[2]**2)
        if view_length > 0:
            view_dir = [view_dir[0]/view_length, view_dir[1]/view_length, view_dir[2]/view_length]
        
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
        
        # Используем только режим Z-буфера
        self.draw_z_buffer(painter)
        
        # Рисуем точки центра букв
        for letter in self.letters:
            if hasattr(letter, 'show_center') and letter.show_center:
                center_point = self.project_point(letter.transformed_center_point)
                if center_point:
                    # Используем красный цвет для точки центра
                    painter.setPen(QPen(Qt.red, 6))
                    painter.setBrush(QColor(255, 0, 0))
                    # Рисуем точку большего размера
                    painter.drawEllipse(center_point, 3, 3)

    def draw_z_buffer(self, painter):
        """Отображение с использованием Z-буфера (имитация)"""
        # Собираем все грани всех букв для Z-буфера
        all_faces = []
        for letter in self.letters:
            for face in letter.faces:
                # Пропускаем невидимые грани
                if not self.is_face_visible(face, letter):
                    continue
                
                depth = self.get_face_depth(face, letter)
                color = self.get_face_color(face, letter)
                
                # Усиливаем контраст в цвете для Z-буфера
                enhanced_color = []
                for c in color:
                    enhanced_color.append(min(255, int(c * 1.2)))
                
                # Преобразуем вершины грани в экранные координаты
                screen_vertices = []
                all_vertices_visible = True
                
                for vertex in face['vertices']:
                    if isinstance(vertex, list):
                        # Это локальные координаты
                        local_vertex = vertex
                        global_vertex = [
                            local_vertex[0] + letter.position[0],
                            local_vertex[1] + letter.position[1],
                            local_vertex[2] + letter.position[2]
                        ]
                        screen_pos = self.project_point(global_vertex)
                    else:
                        # Это индекс вершины в списке transformed_vertices
                        global_vertex = letter.transformed_vertices[vertex]
                        screen_pos = self.project_point(global_vertex)
                    
                    if screen_pos:
                        screen_vertices.append(screen_pos)
                    else:
                        all_vertices_visible = False
                        break
                
                # Добавляем грань только если все её вершины видимы и их достаточно для полигона
                if all_vertices_visible and len(screen_vertices) >= 3:
                    all_faces.append({
                        'screen_vertices': screen_vertices,
                        'depth': depth,
                        'color': enhanced_color,
                        'letter': letter
                    })
        
        # Сортируем грани по глубине (от дальних к ближним)
        all_faces.sort(key=lambda f: f['depth'], reverse=True)
        
        # Рисуем грани в порядке от дальних к ближним
        for face in all_faces:
            points = face['screen_vertices']
            color = face['color']
            
            if len(points) < 3:
                continue  # Пропускаем, если недостаточно точек для полигона
                
            # Создаем полигон для отрисовки
            polygon = QPolygon()
            for point in points:
                polygon.append(point)
            
            # Рисуем заливку если включено отображение граней
            if self.show_faces:
                # Используем высокую непрозрачность для лучшей визуализации
                face_color = QColor(color[0], color[1], color[2], self.fill_opacity)
                painter.setBrush(face_color)
                painter.setPen(Qt.NoPen)
                painter.drawPolygon(polygon)
            
            # Рисуем контур грани если включено отображение рёбер
            if self.show_edges:
                edge_color = QColor(color[0], color[1], color[2])
                edge_color.setAlpha(255)  # Полностью непрозрачные рёбра
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(edge_color, self.edge_thickness))
                painter.drawPolygon(polygon)

    def get_face_color(self, face, letter):
        """Вычисляет цвет грани в зависимости от освещения"""
        # Базовый цвет в зависимости от типа буквы
        if letter.letter == 'С':
            base_color = [100, 100, 255]  # Синий для буквы С
        else:
            base_color = [255, 100, 100]  # Красный для буквы Д
        
        # Вычисляем нормаль грани в мировых координатах
        normal = face['normal']
        
        # Направление света (сверху-сзади)
        light_dir = [0, -0.5, -1]
        # Нормализуем направление света
        light_length = math.sqrt(light_dir[0]**2 + light_dir[1]**2 + light_dir[2]**2)
        light_dir = [light_dir[0]/light_length, light_dir[1]/light_length, light_dir[2]/light_length]
        
        # Вычисляем косинус угла между нормалью и направлением света
        dot_product = abs(normal[0] * light_dir[0] + normal[1] * light_dir[1] + normal[2] * light_dir[2])
        
        # Коэффициент освещенности (от 0.3 до 1.0, чтобы не было полностью черных граней)
        light_factor = 0.3 + 0.7 * dot_product
        
        # Применяем освещение к базовому цвету
        color = [
            min(255, int(base_color[0] * light_factor)),
            min(255, int(base_color[1] * light_factor)),
            min(255, int(base_color[2] * light_factor))
        ]
        
        return color

    def mousePressEvent(self, event):
        self.last_pos = QPoint(int(event.position().x()), int(event.position().y()))
        self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if not self.mouse_pressed:
            return
            
        current_pos = QPoint(int(event.position().x()), int(event.position().y()))
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
                # После перемещения обновляем трансформированные вершины
                self.selected_letter.update_geometry()
        
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
            # После перемещения обновляем трансформированные вершины
            self.selected_letter.update_geometry()
            self.update()

    def reflect_selected(self, axis):
        """Отражает выбранную букву по указанной оси"""
        if self.selected_letter:
            self.selected_letter.reflect(axis)
            self.update()

    def rotate_selected(self, axis, direction):
        """Вращает выбранную букву вокруг указанной оси"""
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

    def set_render_mode(self, mode):
        """Устанавливает режим отображения"""
        self.render_mode = mode
        self.update()
    
    def toggle_faces(self, show):
        """Включает/выключает отображение заливки граней"""
        print(f"ViewerWidget: toggling faces to {show}")
        self.show_faces = show
        self.update()
    
    def toggle_edges(self, show):
        """Включает/выключает отображение рёбер"""
        print(f"ViewerWidget: toggling edges to {show}")
        self.show_edges = show
        self.update()
    
    def set_fill_opacity(self, opacity):
        """Устанавливает непрозрачность заливки"""
        self.fill_opacity = opacity
        self.update()
    
    def set_edge_thickness(self, thickness):
        """Устанавливает толщину рёбер"""
        self.edge_thickness = thickness
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
        
        # Выбор активной буквы
        letter_selector_group = QGroupBox("Выбор буквы")
        letter_selector_layout = QVBoxLayout(letter_selector_group)
        self.letter_combo = QComboBox()
        self.letter_combo.addItems(["Буква С", "Буква Д"])
        self.letter_combo.currentIndexChanged.connect(self.change_selected_letter)
        letter_selector_layout.addWidget(self.letter_combo)
        control_layout.addWidget(letter_selector_group)
        
        # Группа параметров букв
        self.letter_params_group = QGroupBox("Параметры букв")
        letter_params_layout = QVBoxLayout(self.letter_params_group)
        
        # Параметры для буквы С
        self.c_params_widget = QWidget()
        c_params_layout = QVBoxLayout(self.c_params_widget)
        c_params_layout.setContentsMargins(0, 0, 0, 0)
        
        # Высота для С
        c_height_layout = QHBoxLayout()
        c_height_layout.addWidget(QLabel("Высота:"))
        self.c_height_spin = QDoubleSpinBox()
        self.c_height_spin.setRange(0.1, 20.0)
        self.c_height_spin.setValue(4.0)
        self.c_height_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_height_layout.addWidget(self.c_height_spin)
        c_params_layout.addLayout(c_height_layout)
        
        # Ширина для С
        c_width_layout = QHBoxLayout()
        c_width_layout.addWidget(QLabel("Ширина:"))
        self.c_width_spin = QDoubleSpinBox()
        self.c_width_spin.setRange(0.1, 20.0)
        self.c_width_spin.setValue(2.0)
        self.c_width_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_width_layout.addWidget(self.c_width_spin)
        c_params_layout.addLayout(c_width_layout)
        
        # Глубина для С
        c_depth_layout = QHBoxLayout()
        c_depth_layout.addWidget(QLabel("Глубина:"))
        self.c_depth_spin = QDoubleSpinBox()
        self.c_depth_spin.setRange(0.1, 20.0)
        self.c_depth_spin.setValue(1.0)
        self.c_depth_spin.valueChanged.connect(lambda: self.update_letter_params("С"))
        c_depth_layout.addWidget(self.c_depth_spin)
        c_params_layout.addLayout(c_depth_layout)
        
        # Параметры для буквы Д
        self.d_params_widget = QWidget()
        d_params_layout = QVBoxLayout(self.d_params_widget)
        d_params_layout.setContentsMargins(0, 0, 0, 0)
        
        # Высота для Д
        d_height_layout = QHBoxLayout()
        d_height_layout.addWidget(QLabel("Высота:"))
        self.d_height_spin = QDoubleSpinBox()
        self.d_height_spin.setRange(0.1, 20.0)
        self.d_height_spin.setValue(4.0)
        self.d_height_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_height_layout.addWidget(self.d_height_spin)
        d_params_layout.addLayout(d_height_layout)
        
        # Ширина для Д
        d_width_layout = QHBoxLayout()
        d_width_layout.addWidget(QLabel("Ширина:"))
        self.d_width_spin = QDoubleSpinBox()
        self.d_width_spin.setRange(0.1, 20.0)
        self.d_width_spin.setValue(2.0)
        self.d_width_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_width_layout.addWidget(self.d_width_spin)
        d_params_layout.addLayout(d_width_layout)
        
        # Глубина для Д
        d_depth_layout = QHBoxLayout()
        d_depth_layout.addWidget(QLabel("Глубина:"))
        self.d_depth_spin = QDoubleSpinBox()
        self.d_depth_spin.setRange(0.1, 20.0)
        self.d_depth_spin.setValue(1.0)
        self.d_depth_spin.valueChanged.connect(lambda: self.update_letter_params("Д"))
        d_depth_layout.addWidget(self.d_depth_spin)
        d_params_layout.addLayout(d_depth_layout)
        
        # Добавляем виджеты параметров в группу
        letter_params_layout.addWidget(self.c_params_widget)
        letter_params_layout.addWidget(self.d_params_widget)
        
        # По умолчанию показываем параметры для первой буквы
        self.d_params_widget.hide()
        
        control_layout.addWidget(self.letter_params_group)

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
        
        # Группа настройки отображения (Этап 2)
        render_group = QGroupBox("Настройки отображения (Этап 2)")
        render_layout = QVBoxLayout(render_group)
        
        # Выбор режима отображения
        render_mode_layout = QHBoxLayout()
        render_mode_layout.addWidget(QLabel("Режим отображения:"))
        self.render_mode_combo = QComboBox()
        self.render_mode_combo.addItems(["Каркас (wireframe)", "Сортировка по глубине (depth-sort)", "Z-буфер (z-buffer)"])
        self.render_mode_combo.setCurrentIndex(0)  # По умолчанию - каркас
        self.render_mode_combo.currentIndexChanged.connect(self.change_render_mode)
        render_mode_layout.addWidget(self.render_mode_combo)
        render_layout.addLayout(render_mode_layout)
        
        # Флажки для отображения граней и рёбер
        self.show_faces_check = QCheckBox("Показывать грани")
        self.show_faces_check.setChecked(self.viewer.show_faces)
        self.show_faces_check.stateChanged.connect(self.toggle_faces)
        render_layout.addWidget(self.show_faces_check)
        
        self.show_edges_check = QCheckBox("Показывать рёбра")
        self.show_edges_check.setChecked(self.viewer.show_edges)
        self.show_edges_check.stateChanged.connect(self.toggle_edges)
        render_layout.addWidget(self.show_edges_check)
        
        # Настройка непрозрачности заливки
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Непрозрачность заливки:"))
        opacity_spin = QSpinBox()
        opacity_spin.setRange(0, 255)
        opacity_spin.setValue(self.viewer.fill_opacity)
        opacity_spin.valueChanged.connect(self.viewer.set_fill_opacity)
        opacity_layout.addWidget(opacity_spin)
        render_layout.addLayout(opacity_layout)
        
        # Настройка толщины рёбер
        edge_thickness_layout = QHBoxLayout()
        edge_thickness_layout.addWidget(QLabel("Толщина рёбер:"))
        edge_thickness_spin = QSpinBox()
        edge_thickness_spin.setRange(1, 5)
        edge_thickness_spin.setValue(self.viewer.edge_thickness)
        edge_thickness_spin.valueChanged.connect(self.viewer.set_edge_thickness)
        edge_thickness_layout.addWidget(edge_thickness_spin)
        render_layout.addLayout(edge_thickness_layout)
        
        # Добавляем все группы в панель управления
        control_layout.addWidget(movement_group)
        control_layout.addWidget(rotation_group)
        control_layout.addWidget(scale_group)
        control_layout.addWidget(reflection_group)
        control_layout.addWidget(render_group)  # Добавляем новую группу для Этапа 2
        
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
        self.step_spin = step_spin
        self.rotation_step_spin = rotation_step_spin
        self.scale_spin = scale_spin
        self.opacity_spin = opacity_spin
        self.edge_thickness_spin = edge_thickness_spin
        
        # Инициализируем выбор активной буквы
        self.change_selected_letter(0)
        # Инициализируем режим отображения
        self.change_render_mode(0)  # По умолчанию - каркас
        
    def change_selected_letter(self, index):
        # Выбираем букву
        if index == 0:  # Буква С
            self.viewer.selected_letter = self.viewer.letters[0]
            self.c_params_widget.show()
            self.d_params_widget.hide()
        else:  # Буква Д
            self.viewer.selected_letter = self.viewer.letters[1]
            self.c_params_widget.hide()
            self.d_params_widget.show()
        self.viewer.update()
    
    def change_render_mode(self, index):
        # Изменяем режим отображения
        modes = ["wireframe", "depth-sort", "z-buffer"]
        self.viewer.set_render_mode(modes[index])
        # Обновляем UI в зависимости от режима
        self.update_display_settings_ui(modes[index])
    
    def update_display_settings_ui(self, mode):
        # Обновляем UI в зависимости от режима отображения
        if mode == "wireframe":
            # В режиме каркаса грани не отображаются
            self.show_faces_check.setChecked(False)
            self.show_faces_check.setEnabled(False)
            self.opacity_spin.setEnabled(False)
            
            # Рёбра всегда включены в режиме каркаса
            self.show_edges_check.setChecked(True)
            self.show_edges_check.setEnabled(False)
            self.edge_thickness_spin.setEnabled(True)
        else:
            # В других режимах все настройки доступны
            self.show_faces_check.setEnabled(True)
            self.opacity_spin.setEnabled(True)
            self.show_edges_check.setEnabled(True)
            self.edge_thickness_spin.setEnabled(True)
    
    def toggle_faces(self, state):
        # Включаем/выключаем отображение граней
        show = state == Qt.Checked
        print(f"MainWindow: toggling faces to {show}, state={state}")
        self.viewer.toggle_faces(show)
        
    def toggle_edges(self, state):
        # Включаем/выключаем отображение рёбер
        show = state == Qt.Checked
        print(f"MainWindow: toggling edges to {show}, state={state}")
        self.viewer.toggle_edges(show)

    def update_letter_params(self, letter):
        if letter == "С" and self.viewer.letters[0]:
            self.viewer.letters[0].height = self.c_height_spin.value()
            self.viewer.letters[0].width = self.c_width_spin.value()
            self.viewer.letters[0].depth = self.c_depth_spin.value()
            self.viewer.letters[0].update_geometry()
        elif letter == "Д" and self.viewer.letters[1]:
            self.viewer.letters[1].height = self.d_height_spin.value()
            self.viewer.letters[1].width = self.d_width_spin.value()
            self.viewer.letters[1].depth = self.d_depth_spin.value()
            self.viewer.letters[1].update_geometry()
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
