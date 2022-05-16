<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Tarea</title>
</head>
<body>
 
    <% 
        sel_pte = sel_done = '' 
        if old[1] == True:
           sel_pte = 'selected'
        else:
            sel_done = 'selected'
        end
    %>
    <form action="/edit/{{no}}" method="POST">
      <input type="text" name="task" value="{{old[0]}}" size="100" maxlength="100">
      <select name="status">
        
        <option {{sel_pte}}>pendiente</option>
        <option {{sel_done}}>finalizada</option>
      </select>
      <br>
      <input type="submit" name="save" value="save">
    </form>   
</body>
</html>