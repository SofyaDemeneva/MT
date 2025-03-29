import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QComboBox
from PySide6.QtGui import QColor, QPainter, QPen, QStandardItemModel, QStandardItem, QFont, QBrush
from PySide6.QtCore import Qt

# Определение функций
def func1(x):
    return 5 * np.sin(x)  # Возвращает 5 умноженное на синус x

def func2(x):
    return np.log(abs(x) + 1) * np.sin(5*x) * 3  # Возвращает логарифм от модуля x + 1, умноженный на синус 5x и 3

def func3(x):
    with np.errstate(divide='ignore', invalid='ignore'):  # Игнорируем деление на ноль и недопустимые операции
        y = np.where(x != 2, 5 / (x - 2), np.nan)  # Возвращает 5 / (x - 2), если x не равно 2, иначе NaN
    return y

FUNCTIONS = {
    "5 * sin(x)": func1,  # Словарь функций
    "log(|x| + 1) * sin(5x) * 3": func2,
    "5 / (x - 2)": func3
}

COLORS = [QColor(255, 0, 0), QColor(0, 0, 255), QColor(0, 200, 0)]  # Список цветов для функций

class MultiSelectComboBox(QComboBox):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса
        self.setEditable(True)  # Устанавливаем возможность редактирования
        self.model = QStandardItemModel(self)  # Создаем модель для элементов
        self.setModel(self.model)  # Устанавливаем модель
        self.lineEdit().setReadOnly(True)  # Устанавливаем поле для ввода только для чтения
        self.lineEdit().setText("Выберите функции")  # Устанавливаем текст в поле для ввода
        self.view().pressed.connect(self.toggle_item)  # Подключаем событие нажатия к функции toggle_item

    def add_checkable_item(self, text):
        item = QStandardItem(text)  # Создаем элемент с текстом
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)  # Устанавливаем флаги для возможности выбора и включения
        item.setData(Qt.Unchecked, Qt.CheckStateRole)  # Устанавливаем состояние элемента как невыбранное
        self.model.appendRow(item)  # Добавляем элемент в модель

    def toggle_item(self, index):
        item = self.model.itemFromIndex(index)  # Получаем элемент по индексу
        item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)  # Переключаем состояние элемента
        self.update_text()  # Обновляем текст в поле для ввода

    def get_selected_items(self):
        return [self.model.item(i).text() for i in range(self.model.rowCount()) if self.model.item(i).checkState() == Qt.Checked]  # Возвращаем список выбранных элементов

    def update_text(self):
        selected_texts = self.get_selected_items()  # Получаем список выбранных элементов
        self.lineEdit().setText(", ".join(selected_texts) if selected_texts else "Выберите функции")  # Обновляем текст в поле для ввода

class PlotWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)  # Инициализация родительского класса
        self.selected_functions = []  # Список выбранных функций
        self.x_range = (-10, 10)  # Диапазон значений x
        self.num_points = 10  # Фиксированное количество точек

    def set_params(self, functions, x_range):
        self.selected_functions = functions  # Устанавливаем выбранные функции
        self.x_range = x_range  # Устанавливаем диапазон значений x
        self.update()  # Обновляем виджет

    def paintEvent(self, event):
        painter = QPainter(self)  # Создаем объект QPainter
        painter.setRenderHint(QPainter.Antialiasing)  # Включаем сглаживание
        width, height = self.width(), self.height()  # Получаем ширину и высоту виджета
        start, end = self.x_range  # Получаем начальное и конечное значение x

        # Устанавливаем отступы для сетки
        margin = 50
        grid_width = width - 2 * margin  # Ширина сетки
        grid_height = height - 2 * margin  # Высота сетки

        # Вычисляем шаг на основе фиксированного количества точек
        step_x = (end - start) / (self.num_points - 1)

        x = np.linspace(start, end, self.num_points)  # Создаем массив значений x
        y_values = {func_name: FUNCTIONS[func_name](x) for func_name in self.selected_functions}  # Вычисляем значения y для выбранных функций
        if not y_values:
            return

        # Фильтрация бесконечных значений
        finite_y_values = {k: v[np.isfinite(v)] for k, v in y_values.items()}  # Фильтруем бесконечные значения

        if not finite_y_values:
            return

        x_min, x_max = min(x), max(x)
        y_min = min([np.nanmin(y) for y in finite_y_values.values()])
        y_max = max([np.nanmax(y) for y in finite_y_values.values()])
        x_min -= step_x
        x_max += step_x
        y_min -= 1
        y_max += 1

        scale_x = grid_width / (x_max - x_min)  # Масштаб по x
        scale_y = grid_height / (y_max - y_min)  # Масштаб по y

        painter.setPen(QPen(QColor(220, 220, 220), 1, Qt.DashLine))  # Устанавливаем стиль пера для сетки
        for i in range(self.num_points + 1):  # Рисуем вертикальные линии сетки только в пределах заданной области
            x_pos = int((x_min + i * step_x - x_min) * scale_x) + margin  # Вычисляем позицию по x
            painter.drawLine(x_pos, margin, x_pos, height - margin)  # Рисуем вертикальные линии сетки
        for i in range(int(np.floor(y_min)), int(np.ceil(y_max)) + 1):
            y_pos = height - margin - int((i - y_min) * scale_y)  # Вычисляем позицию по y
            painter.drawLine(margin, y_pos, width - margin, y_pos)  # Рисуем горизонтальные линии сетки

        # Рисуем границы сетки
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawRect(margin, margin, grid_width, grid_height)

        painter.setPen(QPen(Qt.black, 2))  # Устанавливаем стиль пера для осей
        x0 = margin - x_min * scale_x  # Позиция оси x
        y0 = height - margin - (0 - y_min) * scale_y  # Позиция оси y
        painter.drawLine(margin, y0, width - margin, y0)  # Рисуем ось x
        painter.drawLine(x0, margin, x0, height - margin)  # Рисуем ось y

        label_offset = 20  # Отступ для подписей
        painter.setFont(QFont("Arial", 10))  # Устанавливаем шрифт для подписей
        for i in range(self.num_points + 1):  # Рисуем подписи по оси x только в пределах заданной области
            x_pos = int((x_min + i * step_x - x_min) * scale_x) + margin  # Вычисляем позицию по x для подписей
            painter.drawText(x_pos + 2, height - margin + label_offset, str(round(x_min + i * step_x, 2)))  # Рисуем подписи по оси x
        for i in range(int(np.floor(y_min)), int(np.ceil(y_max)) + 1):
            y_pos = height - margin - int((i - y_min) * scale_y)  # Вычисляем позицию по y для подписей
            painter.drawText(margin - label_offset - 10, y_pos - 2, str(i))  # Рисуем подписи по оси y

        step_x = grid_width / (self.num_points + 1)  # Вычисляем шаг с учетом дополнительной клетки

        cylinder_width = max(2, grid_width // (self.num_points * 3))  # Уменьшаем ширину цилиндров
        cylinder_depth = max(2, cylinder_width // 2)
        shift_x, shift_y = 30, 30  # Увеличиваем смещение вверх и вправо

        # Рисуем цилиндры для каждой функции
        for i in range(self.num_points):
            x_center = margin + (i + 1) * step_x  # Смещаем цилиндры на одну клетку вправо
            prev_x_center_shifted = x_center
            prev_y_bottom_shifted = None
            for idx, (func_name, y) in enumerate(y_values.items()):
                if np.isfinite(y[i]):
                    color = COLORS[idx % len(COLORS)]  # Устанавливаем цвет для функции
                    painter.setPen(QPen(color.darker(), 1))  # Устанавливаем стиль пера для функции
                    painter.setBrush(QBrush(color, Qt.SolidPattern))  # Устанавливаем кисть для заливки
                    y_bottom = height - margin - (0 - y_min) * scale_y
                    y_top = height - margin - (y[i] - y_min) * scale_y

                    if idx == 0:
                        x_center_shifted = x_center
                        y_top_shifted = y_top
                        y_bottom_shifted = y_bottom
                    else:
                        x_center_shifted = x_center + shift_x * idx
                        y_top_shifted = y_top - shift_y * idx
                        y_bottom_shifted = y_bottom - shift_y * idx

                    # Рисуем прямоугольник с заливкой и цветными границами
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(color, Qt.SolidPattern))
                    painter.drawRect(x_center_shifted - cylinder_width // 2, y_top_shifted, cylinder_width, y_bottom_shifted - y_top_shifted)

                    # Рисуем нижний эллипс на переднем плане с черной границей если значение функции меньше 0
                    painter.setBrush(QBrush(color, Qt.SolidPattern))
                    painter.setPen(QPen(Qt.black, 1) if y[i] < 0 else Qt.NoPen)
                    painter.drawEllipse(x_center_shifted - cylinder_width // 2, y_bottom_shifted - cylinder_depth // 2, cylinder_width, cylinder_depth)

                    # Рисуем верхний эллипс на переднем плане с черными границами если значение функции больше 0
                    painter.setPen(QPen(Qt.black, 1) if y[i] > 0 else Qt.NoPen)
                    painter.setBrush(QBrush(color, Qt.SolidPattern))
                    painter.drawEllipse(x_center_shifted - cylinder_width // 2, y_top_shifted - cylinder_depth // 2, cylinder_width, cylinder_depth)

                    # Соединяем основания прямой линией
                    if idx > 0:
                        painter.setPen(QPen(color.darker(), 1, Qt.SolidLine))
                        painter.drawLine(prev_x_center_shifted, prev_y_bottom_shifted, x_center_shifted, y_bottom_shifted)
                    prev_x_center_shifted = x_center_shifted
                    prev_y_bottom_shifted = y_bottom_shifted

        legend_x = width - 160  # Позиция легенды по x
        legend_y = 10  # Позиция легенды по y
        legend_width = 160  # Ширина легенды
        legend_height = 20 * len(self.selected_functions) + 10  # Высота легенды

        painter.setBrush(QBrush(QColor(255, 255, 255, 255)))  # Устанавливаем кисть для заливки легенды
        painter.setPen(QPen(QColor(0, 0, 0)))  # Устанавливаем стиль пера для рамки легенды
        painter.drawRect(legend_x, legend_y, legend_width, legend_height)  # Рисуем рамку легенды

        painter.setFont(QFont("Arial", 10))  # Устанавливаем шрифт для текста легенды

        for idx, func_name in enumerate(self.selected_functions):  # Рисуем элементы легенды
            color = COLORS[idx % len(COLORS)]  # Устанавливаем цвет элемента легенды
            painter.setPen(QPen(color))  # Устанавливаем стиль пера для элемента легенды
            painter.setBrush(QBrush(color, Qt.SolidPattern))  # Устанавливаем кисть для заливки элемента легенды
            marker_x = legend_x + 10  # Позиция маркера по x
            marker_y = legend_y + 20 * (idx + 1) - 10  # Позиция маркера по y
            painter.drawRect(marker_x, marker_y, 10, 10)  # Рисуем маркер
            painter.drawText(marker_x + 15, legend_y + 20 * (idx + 1), func_name)  # Рисуем текст элемента легенды

class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Инициализация родительского класса
        self.setWindowTitle("Графики с фиксированным количеством точек и цилиндрами")  # Устанавливаем заголовок окна
        self.setGeometry(100, 100, 900, 700)  # Устанавливаем размеры окна
        self.func_combo = MultiSelectComboBox()  # Создаем выпадающий список с возможностью выбора нескольких элементов
        for func_name in FUNCTIONS.keys():
            self.func_combo.add_checkable_item(func_name)  # Добавляем функции в выпадающий список

        self.start_input = QLineEdit("-10")  # Создаем поле для ввода начального значения x
        self.end_input = QLineEdit("10")  # Создаем поле для ввода конечного значения x
        self.plot_button = QPushButton("Построить")  # Создаем кнопку для построения графика
        self.plot_button.clicked.connect(self.plot_chart)  # Подключаем событие нажатия кнопки к функции plot_chart

        input_layout = QHBoxLayout()  # Создаем горизонтальный компоновщик
        input_layout.addWidget(QLabel("Функции:"))  # Добавляем метку "Функции"
        input_layout.addWidget(self.func_combo)  # Добавляем выпадающий список
        input_layout.addWidget(QLabel("От:"))  # Добавляем метку "От"
        input_layout.addWidget(self.start_input)  # Добавляем поле для ввода начального значения x
        input_layout.addWidget(QLabel("До:"))  # Добавляем метку "До"
        input_layout.addWidget(self.end_input)  # Добавляем поле для ввода конечного значения x
        input_layout.addWidget(self.plot_button)  # Добавляем кнопку для построения графика

        main_layout = QVBoxLayout()  # Создаем вертикальный компоновщик
        main_layout.addLayout(input_layout)  # Добавляем горизонтальный компоновщик в вертикальный
        self.plot_widget = PlotWidget(self)  # Создаем виджет для построения графика
        main_layout.addWidget(self.plot_widget)  # Добавляем виджет для построения графика в вертикальный компоновщик

        main_widget = QWidget()  # Создаем основной виджет
        main_widget.setLayout(main_layout)  # Устанавливаем компоновщик для основного виджета
        self.setCentralWidget(main_widget)  # Устанавливаем основной виджет в качестве центрального виджета окна

    def plot_chart(self):
        start = float(self.start_input.text())  # Получаем начальное значение x из поля ввода
        end = float(self.end_input.text())  # Получаем конечное значение x из поля ввода
        selected_funcs = self.func_combo.get_selected_items()  # Получаем список выбранных функций
        if selected_funcs:
            self.plot_widget.set_params(selected_funcs, (start, end))  # Устанавливаем параметры для построения графика

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем приложение
    window = ChartWindow()  # Создаем главное окно
    window.show()  # Показываем главное окно
    sys.exit(app.exec())  # Запускаем цикл обработки событий приложения
