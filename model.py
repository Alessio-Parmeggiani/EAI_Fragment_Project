import open3d as o3d

mesh = o3d.io.read_triangle_mesh("file.stl")
pointcloud = mesh.sample_points_poisson_disk(100000)

# you can plot and check
o3d.visualization.draw_geometries([mesh])
o3d.visualization.draw_geometries([pointcloud])