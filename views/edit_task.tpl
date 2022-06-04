% include('header.tpl', title = "Editar tarea")

    <p>Editar tarea {{no}}:</p>
    <form action="/edit/{{no}}" method="POST">
      <fieldset>
        <div>    
            {{ form.task.label }}:
            {{ form.task }}
            %if form.task.errors:
            <ul class="errors">
                %for error in form.task.errors:
                    <li>{{ error }}</li>
                %end
            </ul>
            %end
        </div>
        <div>
            {{ form.status.label }}:
            {{ form.status }}
        <div>
            {{ form.save }}    
        </div>
    </fieldset>
    </form>   

% include('footer.tpl')