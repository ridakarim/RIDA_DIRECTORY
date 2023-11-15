import tkinter as tk
from itertools import combinations
from math import atan2

class GeometryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Toolbox")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.points = []
        self.lines = []

        self.intersection_label = tk.Label(root, text="Intersection Points:")
        self.intersection_label.pack()

        self.convex_hull_label = tk.Label(root, text="Convex Hull Points:")
        self.convex_hull_label.pack()

        self.check_intersection_button = tk.Button(root, text="Check Intersection", command=self.check_intersection)
        self.check_intersection_button.pack()

        self.compute_brute_force_button = tk.Button(root, text="Compute Brute Force Convex Hull", command=self.compute_brute_force_convex_hull)
        self.compute_brute_force_button.pack()

        self.compute_jarvis_march_button = tk.Button(root, text="Compute Jarvis March Convex Hull", command=self.compute_jarvis_march_convex_hull)
        self.compute_jarvis_march_button.pack()

        self.compute_graham_scan_button = tk.Button(root, text="Compute Graham Scan Convex Hull", command=self.compute_graham_scan_convex_hull)
        self.compute_graham_scan_button.pack()

        self.compute_quick_elimination_button = tk.Button(root, text="Compute Quick Elimination Convex Hull", command=self.compute_quick_elimination_convex_hull)
        self.compute_quick_elimination_button.pack()

        self.compute_kirkpatrick_seidel_button = tk.Button(root, text="Compute Kirkpatrick–Seidel Convex Hull", command=self.compute_kirkpatrick_seidel_convex_hull)
        self.compute_kirkpatrick_seidel_button.pack()

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_all)
        self.clear_button.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        point_id = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        self.points.append((x, y))
        self.canvas.tag_bind(point_id, '<Button-1>', lambda event, pid=point_id: self.on_point_click(pid))

    def on_point_click(self, point_id):
        if len(self.points) >= 2:
            line_start, line_end = self.points[-2], self.points[-1]
            line_color = "black"  # Default color
            if len(self.points) % 4 == 0:
                line_color = "red"
            elif len(self.points) % 4 == 2:
                line_color = "blue"

            line_id = self.canvas.create_line(line_start, line_end, fill=line_color)
            self.lines.append((line_start, line_end, line_id))
            self.canvas.tag_lower(line_id)  # Move the line to the background

    def check_intersection(self):
        intersections = []
        for line1, line2 in combinations(self.lines, 2):
            (x1, y1), (x2, y2), _ = line1
            (x3, y3), (x4, y4), _ = line2

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

                if 0 <= t <= 1 and 0 <= u <= 1:
                    intersection_x = x1 + t * (x2 - x1)
                    intersection_y = y1 + t * (y2 - y1)
                    intersections.append((intersection_x, intersection_y))

        if intersections:
            self.intersection_label.config(text=f"Intersection Points: {intersections}")
        else:
            self.intersection_label.config(text="No intersection points.")

    def compute_brute_force_convex_hull(self):
        convex_hull_points = self.brute_force_convex_hull(self.points)
        self.convex_hull_label.config(text=f"Convex Hull Points (Brute Force): {convex_hull_points}")

    def compute_jarvis_march_convex_hull(self):
        convex_hull_points = self.jarvis_march_convex_hull(self.points)
        self.convex_hull_label.config(text=f"Convex Hull Points (Jarvis March): {convex_hull_points}")

    def compute_graham_scan_convex_hull(self):
        convex_hull_points = self.graham_scan_convex_hull(self.points)
        self.convex_hull_label.config(text=f"Convex Hull Points (Graham Scan): {convex_hull_points}")

    def compute_quick_elimination_convex_hull(self):
        convex_hull_points = self.quick_elimination_convex_hull(self.points)
        self.convex_hull_label.config(text=f"Convex Hull Points (Quick Elimination): {convex_hull_points}")

    def compute_kirkpatrick_seidel_convex_hull(self):
        convex_hull_points = self.kirkpatrick_seidel_convex_hull(self.points)
        self.convex_hull_label.config(text=f"Convex Hull Points (Kirkpatrick–Seidel): {convex_hull_points}")

    def kirkpatrick_seidel_convex_hull(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        def upper_tangent(hull1, hull2):
            for i in range(len(hull1) - 1, -1, -1):
                if hull1[i] == hull2[0]:
                    break

            return hull1[i:], hull2[1:]

        def lower_tangent(hull1, hull2):
            for i in range(len(hull1) - 1, -1, -1):
                if hull1[i] == hull2[-1]:
                    break

            return hull1[:i], hull2[:-1]

        def merge_hulls(hull1, hull2):
            upper_tangent_points = upper_tangent(hull1, hull2)
            lower_tangent_points = lower_tangent(hull1, hull2)

            return lower_tangent_points + upper_tangent_points

        def kirkpatrick_seidel_recursive(points):
            if len(points) <= 5:
                return self.graham_scan_convex_hull(points)

            mid = len(points) // 2
            left_hull = kirkpatrick_seidel_recursive(points[:mid])
            right_hull = kirkpatrick_seidel_recursive(points[mid:])

            return merge_hulls(left_hull, right_hull)

        sorted_points = sorted(points)
        convex_hull = kirkpatrick_seidel_recursive(sorted_points)

        return convex_hull

    def brute_force_convex_hull(self, points):
        hull = []
        n = len(points)

        for i in range(n):
            for j in range(i + 1, n):
                is_convex = True
                for k in range(n):
                    if k != i and k != j:
                        x1, y1 = points[i]
                        x2, y2 = points[j]
                        x3, y3 = points[k]
                        cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                        if cross_product < 0:
                            is_convex = False
                            break
                if is_convex:
                    hull.append(points[i])
                    hull.append(points[j])

        return hull

    def jarvis_march_convex_hull(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        n = len(points)
        if n < 3:
            return points

        hull = []
        leftmost = min(points, key=lambda p: p[0])
        hull.append(leftmost)

        current_point = leftmost
        while True:
            endpoint = points[0]
            for i in range(1, n):
                if current_point == endpoint or orientation(current_point, endpoint, points[i]) == -1:
                    endpoint = points[i]
            hull.append(endpoint)
            current_point = endpoint

            if current_point == leftmost:
                break

        return hull

    def graham_scan_convex_hull(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        def graham_scan_sort(points):
            pivot = min(points, key=lambda p: p[1])
            return sorted(points, key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), p))

        n = len(points)
        if n < 3:
            return points

        sorted_points = graham_scan_sort(points)
        hull = [sorted_points[0], sorted_points[1]]

        for i in range(2, n):
            while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != -1:
                hull.pop()
            hull.append(sorted_points[i])

        return hull

    # Add the following method to your GeometryApp class

    def quick_elimination_convex_hull(self, points):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        def quick_elimination_sort(points):
            pivot = min(points, key=lambda p: p[1])
            return sorted(points, key=lambda p: (atan2(p[1] - pivot[1], p[0] - pivot[0]), p))

        def eliminate(points):
            hull = []
            for point in points:
                while len(hull) > 1 and orientation(hull[-2], hull[-1], point) != -1:
                    hull.pop()
                hull.append(point)
            return hull

        n = len(points)
        if n < 3:
            return points

        sorted_points = quick_elimination_sort(points)
        upper_hull = eliminate(sorted_points)
        lower_hull = eliminate(sorted_points[::-1])

        # Concatenate the upper and lower hulls (excluding duplicate points)
        convex_hull = list(set(upper_hull + lower_hull))

        return convex_hull


    def clear_all(self):
        self.points = []
        self.lines = []
        self.canvas.delete("all")
        self.intersection_label.config(text="Intersection Points:")
        self.convex_hull_label.config(text="Convex Hull Points:")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)

    

    root.mainloop()
