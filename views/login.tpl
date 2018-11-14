% include("./views/header.tpl")

<div>

        <h1> Login Page </h1>

        <form action="/login" method="post">
            <p>username:</p> <input name="username" type="text" />
          <p>password:</p> <input name="password" type="password" /> <br/>
            <input value="Login" type="submit" />
        </form>

</div>
% include("./views/footer.tpl")
