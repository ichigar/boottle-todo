% include('header.tpl', title = "registrarse")
<h1>Formulario de registro</h1>
% if form.errors:
<blockquote>
    <p>Hay errores en el formulario:</p>
    <ul>
    % for field, errors in form.errors.items():
        % for error in errors:
        <li class="mark">{{field}}: {{error}}</li>
        % end
    % end
    </ul>
</blockquote>

% end
<form method="POST" action="/register">
    <fieldset>
    <div>
        {{ form.username.label }}:
        {{ form.username }}

    </div>

    <div>
        {{ form.email.label }}:
        {{ form.email }}
    </div>

    <div>
        {{ form.password.label }}:
        {{ form.password }}
    </div>
    <div>
        {{ form.password_confirm.label }}:
        {{ form.password_confirm }}
    </div>

    <div>
        {{ form.accept_rules.label }}:
        {{ form.accept_rules }}
    </div>

    <div>
        {{ form.save }}
        
    </div>
    <div><a href="/" class="btn btn-secondary">Cancelar</a></div>
</fieldset>
</form>
% include('footer.tpl')