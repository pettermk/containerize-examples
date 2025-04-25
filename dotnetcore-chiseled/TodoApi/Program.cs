using Microsoft.EntityFrameworkCore;
using TodoApi.Data; using Testcontainers.PostgreSql;


var builder = WebApplication.CreateBuilder(args);

builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(8000);
});

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Determine connection string
string? connectionString = Environment.GetEnvironmentVariable("DATABASE_URL");

if (string.IsNullOrEmpty(connectionString))
{
    Console.WriteLine("No connection string found. Starting PostgreSQL test container...");

    var postgresContainer = new PostgreSqlBuilder()
        .WithDatabase("todo_db")
        .WithUsername("postgres")
        .WithPassword("password")
        .WithImage("postgres:17-alpine")
        .WithCleanUp(true)
        .WithPortBinding(5432, true) // use dynamic port binding
        .Build();

    await postgresContainer.StartAsync();

    await Task.Delay(2000);
    /*connectionString = postgresContainer.GetConnectionString();*/
    /*connectionString = $"Host={host};Port={port};Username=postgres;Password=password;Database=todo_db";*/
    var port = postgresContainer.GetMappedPublicPort(5432);
    var host = postgresContainer.Hostname;

    Console.WriteLine($"PostgreSQL test container started at: {connectionString}");
    connectionString = $"Host={host};Port={port};Username=postgres;Password=password;Database=todo_db";
}

// Configure PostgreSQL
/*var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");*/

Console.WriteLine($"Attempting to connect to postgres at: {connectionString}");
builder.Services.AddDbContext<TodoDbContext>(options =>
    options.UseNpgsql(connectionString));
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<TodoDbContext>();
    db.Database.Migrate(); // Applies any pending migrations
}


app.UseSwagger();
app.UseSwaggerUI();
app.UseAuthorization();
app.MapControllers();
app.Run();

