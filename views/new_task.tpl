<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/miligram.css">
    <title>Nueva tarea</title>
</head>
<body>
    <p>Añadir una nueva tarea a la lista:</p>
    <form action="/new" method="POST">
      <input type="text" size="100" maxlength="100" name="task">
      <input type="submit" name="save" value="save">
    </form>   
</body>
</html>