import time
import tkinter as tk
from itertools import combinations
from math import atan2
from tkinter import messagebox


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

        self.complexity_label = tk.Label(root, text="Time and Space Complexities:")
        self.complexity_label.pack()


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
    def ccw(self, a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def are_lines_intersecting_ccw(self, line1, line2):
        def intersect(segment1, segment2):
            a, b = segment1
            c, d = segment2
            return self.ccw(a, c, d) != self.ccw(b, c, d) and self.ccw(a, b, c) != self.ccw(a, b, d)

        line1_segment = line1[:2]
        line2_segment = line2[:2]

        return intersect(line1_segment, line2_segment)

    def check_intersection(self):
        intersections = []
        for line1, line2 in combinations(self.lines, 2):
            if self.are_lines_intersecting_ccw(line1, line2):
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
    def display_complexities(self, time_complexity, space_complexity):
        complexity_text = f"Time Complexity: {time_complexity} seconds\nSpace Complexity: {space_complexity}"
        self.complexity_label.config(text=complexity_text)

    def compute_brute_force_convex_hull(self):
        start_time = time.time()
        convex_hull_points = self.brute_force_convex_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_complexity = f"{elapsed_time:.5f}"

        # Assuming convex_hull_points contains the convex hull
        space_complexity = f"{len(convex_hull_points)}"

        self.convex_hull_label.config(text=f"Convex Hull Points (Brute Force): {convex_hull_points}")
        self.display_complexities(time_complexity, space_complexity)

    def compute_jarvis_march_convex_hull(self):
        start_time = time.time()
        convex_hull_points = self.jarvis_march_convex_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_complexity = f"{elapsed_time:.5f}"

        # Assuming convex_hull_points contains the convex hull
        space_complexity = f"{len(convex_hull_points)}"

        self.convex_hull_label.config(text=f"Convex Hull Points (Jarvis March): {convex_hull_points}")
        self.display_complexities(time_complexity, space_complexity)

    def compute_graham_scan_convex_hull(self):
        start_time = time.time()
        convex_hull_points = self.graham_scan_convex_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_complexity = f"{elapsed_time:.5f}"

        # Assuming convex_hull_points contains the convex hull
        space_complexity = f"{len(convex_hull_points)}"

        self.convex_hull_label.config(text=f"Convex Hull Points (Graham Scan): {convex_hull_points}")
        self.display_complexities(time_complexity, space_complexity)

    def compute_quick_elimination_convex_hull(self):
        start_time = time.time()
        convex_hull_points = self.quick_elimination_convex_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_complexity = f"{elapsed_time:.5f}"

        # Assuming convex_hull_points contains the convex hull
        space_complexity = f"{len(convex_hull_points)}"

        self.convex_hull_label.config(text=f"Convex Hull Points (Quick Elimination): {convex_hull_points}")
        self.display_complexities(time_complexity, space_complexity)

    def compute_kirkpatrick_seidel_convex_hull(self):
        start_time = time.time()
        convex_hull_points = self.kirkpatrick_seidel_convex_hull(self.points)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_complexity = f"{elapsed_time:.5f}"

        # Assuming convex_hull_points contains the convex hull
        space_complexity = f"{len(convex_hull_points)}"

        self.convex_hull_label.config(text=f"Convex Hull Points (Kirkpatrick–Seidel): {convex_hull_points}")
        self.display_complexities(time_complexity, space_complexity)

    def check_line_intersection_button(self):
        if len(self.lines) < 4:
            messagebox.showwarning("Not Enough Lines", "Please draw at least two lines.")
            return

        line1 = self.lines[-2][:2]  # Get the last two points of the first line
        line2 = self.lines[-1][:2]  # Get the last two points of the second line

        if self.are_lines_intersecting(line1, line2):
            intersection_point = self.get_intersection_point(line1, line2)
            messagebox.showinfo("Line Intersection", f"The lines intersect at {intersection_point}.")
        else:
            messagebox.showinfo("Line Intersection", "The lines do not intersect.")

    def are_lines_intersecting(self, line1, line2):
        # Implement your line intersection logic here
        # You can use the existing method or add new logic as needed
        pass

    def get_intersection_point(self, line1, line2):
        # Implement the calculation of the intersection point
        # You can use existing code or add new logic as needed
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Calculate intersection point (you can replace this with your existing code)
        intersection_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        intersection_x /= (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        intersection_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        intersection_y /= (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        return round(intersection_x), round(intersection_y)

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
        self.complexity_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)

    root.mainloop()
