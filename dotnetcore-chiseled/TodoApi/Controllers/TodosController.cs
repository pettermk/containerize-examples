// Controllers/TodosController.cs
using Microsoft.AspNetCore.Mvc;
using TodoApi.Models;

namespace TodoApi.Controllers
{
    [ApiController]
    [Route("todos")]
    public class TodosController : ControllerBase
    {
        private static List<Todo> Todos = new();
        private static int CurrentId = 1;

        [HttpPost]
        public ActionResult<Todo> CreateTodo([FromBody] TodoCreate todoCreate)
        {
            var todo = new Todo
            {
                Id = CurrentId++,
                Title = todoCreate.Title,
                Description = todoCreate.Description,
                Completed = todoCreate.Completed,
                CreatedAt = todoCreate.CreatedAt,
                UpdatedAt = todoCreate.UpdatedAt
            };
            Todos.Add(todo);
            return Ok(todo);
        }

        [HttpGet]
        public ActionResult<List<Todo>> ReadTodos([FromQuery] int offset = 0, [FromQuery] int limit = 100)
        {
            return Ok(Todos.Skip(offset).Take(limit).ToList());
        }

        [HttpGet("{todo_id}")]
        public ActionResult<Todo> ReadTodo(int todo_id)
        {
            var todo = Todos.FirstOrDefault(t => t.Id == todo_id);
            if (todo == null) return NotFound();
            return Ok(todo);
        }

        [HttpPatch("{todo_id}")]
        public ActionResult<Todo> UpdateTodo(int todo_id, [FromBody] TodoCreate update)
        {
            var todo = Todos.FirstOrDefault(t => t.Id == todo_id);
            if (todo == null) return NotFound();

            todo.Title = update.Title;
            todo.Description = update.Description;
            todo.Completed = update.Completed;
            todo.UpdatedAt = update.UpdatedAt;

            return Ok(todo);
        }

        [HttpDelete("{todo_id}")]
        public IActionResult DeleteTodo(int todo_id)
        {
            var todo = Todos.FirstOrDefault(t => t.Id == todo_id);
            if (todo == null) return NotFound();

            Todos.Remove(todo);
            return Ok(new { ok = true });
        }
    }
}

