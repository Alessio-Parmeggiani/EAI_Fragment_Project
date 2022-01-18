import os
import re
import open3d as o3d

def pretty_print(grid):
    for row in grid:
        print(row)


def process_file(path):
    with open(path,'r') as f:
        #don't consider first two lines
        f.readline()           #segmenti x x x
        f.readline()           #rotazioni x x x

        line=f.readline()      #numero pezzi x  

        #get number of fragments
        number=int(re.findall("\d+",line)[0])

        #coupling matrix
        grid=[]
        for i in range(number):
            line=f.readline()
            ret=re.findall('-1|0|1',line)
            grid.append(list(map(int,ret)))

        #model data
        model_names=[]
        for m in range(number):
            f.readline()        #blank line
            name=f.readline()   #model name
            f.readline()        #mesh n
            f.readline()        #external n
            f.readline()        #internal n

            #try create file name
            file_name= '_'.join(name.rstrip().split('.'))
            model_names.append(file_name)
            

        return grid,model_names


main_path="produzione_29112021"
for folder in os.listdir(main_path):

    #check only folders
    if '.' not in folder:
        folder_path=os.path.join(main_path,folder)
        models=[]

        #for each set of pieces
        for file in os.listdir(folder_path):
            if '.txt' in file:
                description_file=file
            elif '.stl' in file:
                models.append(file)
        full_description_file=os.path.join(folder_path,description_file)
        grid,model_names=process_file(full_description_file)
        pretty_print(grid)

        model_prefix=folder.replace("generatedTest_","")
        for i in range(len(model_names)):
            model_names[i]=model_prefix+"_"+model_names[i]
        print(model_names)
      
        

        for name in model_names:
            model_path=os.path.join(folder_path,f"{name}.stl")
            mesh = o3d.io.read_triangle_mesh(model_path)
            pointcloud = mesh.sample_points_poisson_disk(1000)

            # you can plot and check
            o3d.visualization.draw_geometries([mesh])
            o3d.visualization.draw_geometries([pointcloud])   
            break


        break


        