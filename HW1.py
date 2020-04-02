import vtk
import numpy as np

# Load Data
# Load points
points = np.genfromtxt('vertices.csv', delimiter=',', skip_header=1) # (X,Y,Z,R,G,B)
triangles = np.genfromtxt('triangles.csv', delimiter=',', dtype=int) # (Point 1, Point 2, Point 3)


# Create Point object
vtk_points_data = vtk.vtkPoints()
# Create color scalars
rgb = vtk.vtkUnsignedCharArray()
# Setting number of scalars, number of colo channels
rgb.SetNumberOfComponents(3)
# Setting name of scalars set
rgb.SetName("Colors")


# Creating id objects for PolyData
vtk_points_topology = vtk.vtkCellArray()
vtk_triangles_topology = vtk.vtkCellArray()

# Setting up PolyData - Vertices
points_list_ids = []
for point_from_list in points:
	points_list_ids.append(vtk_points_data.InsertNextPoint(point_from_list[0],point_from_list[1],point_from_list[2]))
	rgb.InsertNextTuple3(point_from_list[3],point_from_list[4],point_from_list[5])
vtk_points_topology.InsertNextCell(len(points_list_ids),points_list_ids)

# Initializing PolyData (vertices and triangles)
vtk_vertex = vtk.vtkPolyData()
vtk_triangle = vtk.vtkPolyData()

# Set the vertices we created as the geometry and topology of the polydata
vtk_vertex.SetPoints(vtk_points_data)
vtk_vertex.SetVerts(vtk_points_topology)

# Setting triangles
vtk_triangle.SetPoints(vtk_points_data)

# Adding color
vtk_triangle.GetPointData().SetScalars(rgb)
vtk_vertex.GetPointData().SetScalars(rgb)

# Setting up PolyData - Triangles
for triangle_from_list in triangles:
	temp_triangle = vtk.vtkTriangle()
	temp_triangle.GetPointIds().SetId(0,triangle_from_list[0])
	temp_triangle.GetPointIds().SetId(1,triangle_from_list[1])
	temp_triangle.GetPointIds().SetId(2,triangle_from_list[2])
	vtk_triangles_topology.InsertNextCell(temp_triangle)


# Create Mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(vtk_vertex)
vtk_triangle.SetPolys(vtk_triangles_topology)
mapper.SetInputData(vtk_triangle)

# Create and connect Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper) # Passing the mapped source to actor
actor.GetProperty().SetColor(1.0, 0.0, 0.0) # Setting color of the source
# actor.GetProperty().SetRepresentationToSurface()
# actor.GetProperty().LightingOff()
# actor.GetProperty().SetRepresentationToPoints()
actor.GetProperty().SetRepresentationToWireframe()

# Create renderer and passing mapped and acted source to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)
renderer.ResetCamera()

# Create renderer window and passing the render
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName('Scene')
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)

# Create interactor and pass the render window
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
# Initialize the interactor and start the rendering
interactor.Initialize()
render_window.Render()
interactor.Start()

