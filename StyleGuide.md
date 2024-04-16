# Kare coding style guide (intended for C# projects)

###### ***for any feedback please contact Leónidas Neftalí through lcampos@douyoukare.com or any other KARE GDL dev team member***
## Table of contents
- [Introduction](#introduction)
    - [Note:](#note)
- [Formatting guidelines](#formatting-guidelines)
    - [Capitalization](#capitalization)
    - [New Lines](#new-lines)
    - [Indentation](#indentation)
    - [Indentation Depth](#indentation-depth)
    - [Naming conventions](#naming-conventions)
- [Coding guidelines](#coding-guidelines)
    - [Use of inferred types, the `var` keyword](#use-of-inferred-types-the-var-keyword)     
    - [Public methods](#public-methods)
    - [Null checks with value types](#null-checks-with-value-types)
    - [`IDisposable` resources](#-idisposable-resources)
    - [Database operations (ORM)](#database-operations-orm)
    - [Constant fields / local](#constant-fields-local)
    - [Magic numbers / magic strings](#magic-numbers-magic-strings)
    - [Prefer Lowest Common Denominator](#prefer-lowest-common-denominator)
- [Best practices](#best-practices)
    - [Task vs ValueTask](#task-vs-valuetask)
    - [Single await Task](#single-await-task)
    - [Stack vs Heap allocation](#stack-vs-heap-allocation)
    - [String concatenation](#string-concatenation)
    - [Returning multiple values (tuple vs named type)](#returning-multiple-values-tuple-vs-named-type)

## Introduction
This guide aims to provide a standard for Kare Engineers to code in, this standard should be strictly enforced into everyone's code and **WILL BE TAKEN INTO CONSIDERATION FOR ANY PULL REQUESTS**, so please refer to this guide for any reference on examples of how to submit your code.
### Note:
Not all code examples provided here are production-quality code, for the sake of clarity of certain rules we omit optimization / best practices. Please refer to the [Best Practices](#best-practices) section for examples that will be considered "optimal" code.
## Formatting guidelines
### Capitalization
Capitalization on every C# project should follow strict Microsoft design guidelines defined in [their documentation](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/capitalization-conventions). Please find, every identifier type and its capitalization below.
| Identifier | Casing |  Example |
|---|---|---| 
| Namespace | Pascal | `namespace Gst.Kare.Shifts`|
| Type | Pascal | `public class HeroDto`|
| Interface | Pascal | `interface ICommunityAppService`|
| Struct | Pascal | `internal struct CommunityInsertInfo` |
| Method | Pascal | `public void RegisterStatus()` |
| Property | Pascal | `public string Name { get; set; }`|
| Enum value | Pascal | `public enum DayOfWeek {  Monday, Tuesday, Wednesday ... }`|
| Global scoped constant | SNAKE_UPPER | `public class Roles { const string ADMIN_ROLE_NAME = "Admin"; }`|
| Local scoped constant | camelCase | `private void GetAll() { const string adminRoleName = "Admin" }`|
| Static readonly fields | Pascal | `public class Roles { public static readonly string AdminRoleName = "Admin"; }`|
| Parameter | camelCase | `public void GetHero(int id)`|
| Variable | camelCase | `ICommunityFactory factory = new CommunityFactory();`|
| Field | camelCase | `public class User { private string currToken; }`|

### New Lines
In the sake of code clarity and readability, we separate control structures by a new line:
<br/>

**Non compliant code ❌**
```csharp
private void SomeMethod(int id?)
{
    if (id == null)
    {
        ProcessForNull();
    } else {
        ProcessId(id);
    }
}
```
**Compliant code ✔️**
```csharp
private void SomeMethod(int id?)
{
    if (id == null)
    {
        ProcessForNull();
    }
    //Else will be placed in a new line to separate the control structure
    else
    {
        ProcessId(id);
    }
}
```
### Indentation
As a default we recommend **4 spaces** for indentation, if you have a preference for tabs (rightfully so), you can refer to your IDE or code editor to treat spaces tabs or change the indentation on your local instance, however, keep in mind that all code submitted for PR should be converted back to 4 spaces.
### Indentation Depth
Closely related with a best practice we'll explain later in this guide, we recommend an indentation depth of no more than 3 steps. For this, we recommend things like
- Code encapsulation
    - Divide your function's operations into smaller functions
- Design patterns
    - Object creation / queries can increase indentation depth, always use the correct design pattern to avoid surpassing the limit
- Early return
    - If a condition being true validates the rest of your function / loop scope, consider returning / continuing to the next iteration early
<br/>

**Non compliant code ❌**

```csharp
private async ValueTask ProcessData(ICollection<Data> data) 
{
    foreach (Data element in data) 
    {
        if (element != null)
        {
            if (!string.NullOrEmpty(element.name))
            {
                element = await this.dataRepository.InsertAsync(element);
                if (element.Id != null)
                {
                    ...
                }
                else
                {
                    ....
                }
            }
        }
    }
}
```

**Compliant code ✔️**
```csharp
private async ValueTask ProcessData(ICollection<Data> data)
{
    foreach (Data element in data)
    {
        if (element == null || string.NullOrEmpty(element.name))
        {
            continue;
        }
        element = await this.dataRepository.InsertAsync(element);
        if (element.Id != null)
        {
            ...
        }
        else
        {
            ....
        }
    }
}
```
### Naming conventions
There are certain special types of design patterns that require clarification on their naming conventions
- Interfaces
    - Interfaces should always carry the I prefix
    ```csharp 
        public interface IDispatcher 
    ``` 
    - Their implementation should deal away with this prefix, continue with any specific implementation name, and lastly, their inherited interface's name
    ```csharp
        //Example 1
        public class RegionalDispatcher {}
        //Example 2
        public class LocalDispatcher {}
        //Example 3
        public class GlobalDispatcher {}
    ```
- Services
    - Services should be named after the main entity they intend to interact with, followed by any particular implementation specific name, and the word Service
    - **If the Service will be public facing (ABP treats this as a service, but it's essentially a Controller), we should mark it as AppService instead, and make sure it inherits from `KareAppServiceBase` and its own interface**
    ```csharp
        public class CommunityTimeZoneAppService : KareAppServiceBase, ICommunityTimeZoneAppService
        {
            ...
        }
    ```
- Async functions
    - Asynchronous functions should all be marked with the postfix `Async`

    **Non compliant code ❌**
    ```csharp
    public async Task<List<Hero>> GetAllHeroes()
    {
        ...
        return await this.heroRepository.GetAll().ToListAsync();
    }
    ```

    **Compliant code ✔️**
    ```csharp
    public async Task<List<Hero>> GetAllHeroesAsync()
    {
        ...
        return await this.heroRepository.GetAll().ToListAsync();
    }
    ```

## Coding guidelines
We have defined these rules in a separate global `.editorconfig` file, so, if you have any doubt regarding a specific rule, please refer to that file for any clarification.

### Use of inferred types, the `var` keyword
C# provides programmers with the `var` keyword to apply some pretty neat syntactic sugar to their code and omit having to always type their variables, which is fine in a couple of cases, but abusing this feature leads to difficulty reading and infering the code at first sight.
<br/>
We should always avoid using `var` when the type is not immediately apparent from the right-hand side of the assignment.
<br/>

**Non compliant code ❌**
```csharp
private async Task GetAvailableHeroes(int tenantId)
{
    //This is a bad practice because we don't know what type the communities variable will asume
    var communities = await this.GetAllCommunitiesByTenant(tenantId);
    ...
}
```
Notice how even though the `GetAllCommunitiesByTenant` will potentially return some sort of `ICollection<Community>`, we don't know exactly what the collection type will be, we treat Lists very differently from HashSets and from Arrays, in short, not specifying the type of this variable makes it so that future programmers have to navigate to the method's definition, or hover their cursor on top of the variable to discover it, which slows down the programming workflow.
<br/>

**Compliant code #1✔️**
```csharp
private async Task GetAvailableHeroes(int tenantId)
{
    //Now we know we're dealing specifically with a list and can code accordingly
    List<Community> communities = await this.GetAllCommunitiesByTenant(tenantId);
    ...
}
```
Now, that does not mean that `var` is completely forbidden, in fact, we encourage its **proper** use, as we know types in C# can be a mouthful. Which is why `var` should be used when the type is apparent from the right hand side of the assignment,

**Compliant code #2✔️**
```csharp
private async Task GetAvailableHeroes(int tenantId)
{
    var communitiesMapById = new Dictionary<int, Community>();
    ...
}
```
This way we avoid having to write `Dictionary<int, Community>` twice in the declaration and assignment.

<br/>

Note that the only exception to this last rule is when dealing with primitives, **primitives should always be typed on the left**

**Non compliant code ❌**

```csharp
var age = 18;
```

**Compliant code ✔️**
```csharp
int age = 18;
```
### Public methods
For any methods that will be interacting publicly there are a few rules to follow.
- If applicable, the method should be derived from the base interface
- Make sure the interface and implementation methods have matching parameter names
- Always document your methods and arguments using the XML documentation syntax

### Null checks with value types
Often when trying to validate parameters or data coming from the database we need to perform null checks, this however gets potentially tricky when dealing with value types (structs and primitives), for example:

**Non compliant code ❌**
```csharp
//Value type used to keep user information
internal struct UserRecord
{
    string name;
    int age;
}

public void DoSomething(UserRecord user)
{
    //This condition will never be true even if the user parameter is not initialized
    if (user == null)
    {
        return;
    }
}
```
Because structs are value types, comparing them to null (a reference type) will be useless, instead, we have two options, either compare them with the `default` operator, or make them nullable **(keep in mind this WILL PERFORM A HEAP ALLOCATION)**

**Compliant code #1 ✔️**
```csharp
//Value type used to keep user information
internal struct UserRecord
{
    string name;
    int age;
}

public void DoSomething(UserRecord user)
{
    if (user == default)
    {
        return;
    }
}
```

**Compliant code #2 (with heap allocation) ✔️**

```csharp
//Value type used to keep user information
internal struct UserRecord
{
    string name;
    int age;
}

public void DoSomething(UserRecord? user)
{
    if (user == null)
    {
        return;
    }
}
```
### `IDisposable` resources
A disposable resource is an instance of a class that implements the `IDisposable` interface, and refers to a code resource that either allocates memory and needs manual indication of when it should be cleared out, or accesses IO / Network resources that need to be properly closed when no longer using the object, a couple of examples of disposable classes are

- Database connections
- File handles
- Serial connections
- Data Streams

Every disposable resource needs to be disposed manually and consciously, and since doing `.Dispose();` at the end of a function is easy to forget, we encourage to always follow the `using` syntax for correctly handling these connections

**Compliant code ✔️**
```csharp
public void ProcessImage(byte[] imageBytes)
{
    //Opening the resource with its constructor
    using (var imageStream = new MemoryStream(imageBytes))
    {
        ...
    } //imageStream will call Dispose() here automatically
}
```

### Database operations (ORM)
Using Raw SQL is **highly** discouraged, both for security and readability reasons, we should always prefer an Object Relational Model approach (ORM), and along that line let's look at general rules over database operations
- Always follow the repository pattern
    - ABP provides a default `IRepository` interface which can and should be used for simple data querying / inserting and updating. Although, the implemented version does NOT support bulk insert / bulk update operations
    - For bulk insert / bulk update operations, please use the custom-made `BulkRepository` class.
- LinQ extension vs SQL-like syntax
    - When performing queries through a repository, always use the LinQ extension syntax as it improves readability and mantainability of its operations.
    
    **Non compliant code ❌**

    ```csharp
    IQueryable<long> userIds = from t1 in _userRepository.Value.GetAll()
              where t1.TenantId == null
              && t1.Hero == null
              && t1.IsActive
              && t1.IsRemove == false
              && t1.Roles.Any(n => kareRoleIds.Contains(n.RoleId))
              select t1.Id;
    ```

    **Compliant code ✔️**

    ```csharp
    IQueryable<long> userIds = _userRepository.Value.GetAll()
        .Where(
                userFromDb => userFromDb.TenantId == null &&
                userFromDb.Hero == null &&
                userFromDb.IsActive &&
                userFromDb.IsRemove == false &&
                userFromDb.Roles.Any(role => kareRoleIds.Contains(role.RoleId))
            );
    ```
    ***Performance note***

    *ORM operations using the LINQ extension syntax are more likely to be avaluated in memory if C# finds any operation that cannot be executed on the Database end, so, please restrict your queries to only simple logical operations such as:*
    - Logical comparisons (`valueFromDb || valueToCheck`, `valueFromDb && valueToCheck`).
    - Contains operations on `IList`.
    - Joins using the LINQ syntax

    *Please refrain from doing the following as they can cause the runtime to load the DB contents in memory*
    - Custom function evaluations
    - Complex DataStructure operations
    - Calls to libraries
    - Bitwise operations

- Avoid asynchronous operations in a loop
    - Sometimes, we need to perform an async operation many times over a certain collection, maybe run some logic inside each iteration and then query the database based on that. It might be tempting then to simply call your queries as if they were synchronous operations, however, keep in mind this has a **huge** impact on performance, it drastically slows down processing time, and we know that means two things, bad user experience, and a higher AWS bill.

    **Non compliant code ❌**
    ```csharp
    foreach (var item in input.CommunityRoles)
    {
        var communityHeroRole = communityHeroRoleList.FirstOrDefault(n => n.HeroRoleId == item.HeroRoleId);
        if (communityHeroRole == null)
        {
            item.TenantId = AbpSession.TenantId.Value;
            await _communityHeroRoleRepository.Value.InsertAsync(ObjectMapper.Map<CommunityHeroRole>(item));
        }
        else
        { 
        ....
        }
    }    
    ```

    **Compliant code ✔️**

    ```csharp
    //Create a list for the items we want to insert asynchronously
    var rolesToInsert = new List<CommunityHeroRole>(); 

    foreach (CommunityHeroRoleDto item in input.CommunityRoles)
    {
        CommunityHeroRoleDto communityHeroRole = communityHeroRoleList.FirstOrDefault(n => n.HeroRoleId == item.HeroRoleId);
        if (communityHeroRole == null)
        {
            item.TenantId = AbpSession.TenantId.Value;
            //Create the HeroRole entity from the DTO mapper
            CommunityHeroRole toInsert = Map<CommunityHeroRole>(item);
            //Add it to the insertion list (DO NOT PERFORM ANY DB QUERIES)
            rolesToInsert.Add(toInsert);
            continue;
        }
        ....
    }
    //Here _communityHeroRoleRepository should be of type BulkRepository<T> 
    await _communityHeroRoleRepository.Value.InsertManyAsync(rolesToInsert);
    ```

### Constant fields / local
We already discussed the style and capitalization around constants, so, let's now go over some of the rules associated with them.

TLDR: **IF IT COULD BE A CONSTANT, MAKE IT A CONSTANT**

For primitives that will be used multiple times across a global context, always declare them as `const` at the top of the class. In case the value you need is a reference type (classes), you can declare them as a `static readonly T Foo = new Foo();` to make sure we allocate its memory exactly once.

On local scopes, if a value is declared as a variable but we never modify it, it should be declared as constant

**Non compliant code ❌**
```csharp
public void LogMessage(string message) {
    string prefix = "[Info] - "
    this.logger.Info($"{prefix} {message}");
}
```

**Compliant code ✔️**
```csharp
public void LogMessage(string message) {
    //Mark as const, since we don't modify it throughout the whole scope
    const string prefix = "[Info] - "
    this.logger.Info($"{prefix} {message}");
}
```

### Magic numbers / magic strings
Magic values are those values which are crucial for an operation to work, but their purpose is not exaplained... this is one of the **HIGHEST** priority code smells this guide attempts to tackle, and the tolerance for it is low.

**Non compliant code ❌**
```csharp
public static void OverrideSSNInput(this PdfContentByte under, string subString, float initalX)
{
    float initX = initalX;
    foreach (var item in subString)
    {
        //Notice the magic numbers below
        under.OverrideW9Input(item.ToString(), initX, 438, 10, 12, 440);
        initX += 14;
    }
}
```

**Compliant code ✔️**

```csharp
//Declaring constants
const float OFFSET_STEP_X = 14f;
const float RECT_FIXED_POS_Y = 438f;
const float RECT_WIDTH = 10f;
const float RECT_HEIGTH = 12f;
const float TEXT_FIXED_POS_Y = 440f;

public static void OverrideSSNInput(this PdfContentByte under, string subString, float initalX)
{
    float initX = initalX;
    foreach (char item in subString)
    {
        //Notice the magic numbers below
        under.OverrideW9Input(item.ToString(), initX, RECT_FIXED_POS_Y, RECT_WIDTH, RECT_HEIGTH, TEXT_FIXED_POS_Y);
        initX += OFFSET_STEP_X;
    }
}
```
By declaring the constants we get more context at first sight about what those values mean and how they're used in the context of the function we're passing them to

### Prefer Lowest Common Denominator
Either for returning or passing values throughout the program, we always need to try and make every part of our system completely independent from one another, due to SOLID principles (which, we don't necessarily say we have to follow 100% of the time, otherwise the code would be absolutely unreadable). This is why we encourage that every time you need to get a parameter whose class derives from an interface or a parent class, please always attempt to use the lowest common denominator. i.e, for a `List` use `IEnumerable` if we only care about the elements, its count, etc, if we do want more "list specific stuff" we go up the hierarchy to `ICollection` then `IList` and then as a last resort the full implementation class `List` 

## Best practices

### Task vs ValueTask
When declaring a function that makes use of asynchronous operations it's common to use the `Task<T>` class to indicate C# that it should be awaited, however, sometimes we have a base validation that, if failed we simply stop all processing and either return or throw an error.

For such methods, we insist changing the return type from `Task<T>` to `ValueTask<T>` which is a *value type* that can be stack allocated by C#, not only that, but `ValueTask<T>` makes sure that if we fail those validations we don't create a new `Task` object, which vastly reduces the overhead of our methods.

**Non compliant code ❌**
```csharp
public Task<bool> UserExistsAsync(string userName)
{
    if (string.IsNullOrEmpty())
    {
        return false;
    }
    return this.userRepository.GetAll()
        .Where(userFromDb => userFromDb.UserName == userName)
        .AnyAsync();
}
```

**Compliant code ✔️**
```csharp
//Change the return type since we don't always reach the await call
public ValueTask<bool> UserExistsASync(string userName)
{
    if (string.IsNullOrEmpty())
    {
        return false;
    }
    return this.userRepository.GetAll()
        .Where(userFromDb => userFromDb.UserName == userName)
        .AnyAsync();
}
```

### Single await Task
When dealing with methods that only perform exactly one asynchronous operation, the `await` keyword is not needed, and it fact could compromise performance, so, make sure to include the keyword only when multiple operations are being performed, and simply defer the `await` call to the top-level caller method.

**Non compliant code ❌**
```csharp
public async Task<bool> UserExistsAsync(string userName)
{
    return await this.userRepository.GetAll()
        .Where(userFromDb => userFromDb.UserName == userName)
        .AnyAsync();
}
```

**Compliant code ✔️**

```csharp
//Deleted the async keyword here since no await is needed
public Task<bool> UserExistsAsync(string userName)
{
    //Deleted the await keyword
    return this.userRepository.GetAll()
        .Where(userFromDb => userFromDb.UserName == userName)
        .AnyAsync();
}
...
private async Task ControllerMethod(string userName) {
    //Defer the await keyword to the caller method
    bool exists = await this.userService.UserExistsAsync();
}
```

### Stack vs Heap allocation
The stack and the heap are methods for storing data in RAM, the stack section is generally a small area of linear memory, this means, if you allocate `int[] a = {5, 6, 2};` you'll guarantee that 2 is right next to 6 which is right next to 5 in the physical memory space, this is great because memory that is close together is easier to allocate, and easier to access. However, the stack is not magical, as it has its limitations, mainly that **you need to know the size of everything you want to allocate, before running the program** so it's only good for compile-time allocations.

To solve this issue, we have dynamic memory, AKA. the heap, which is a larger area in RAM that can shrink and grow depending on your needs, the main issue with the heap is that since it needs to constantly change it means memory is **not** guaranteed to be allocated closely and linearly, and even worse, each call to the heap whether to create something (`new` keyword) or to destroy something (garbage collector calls), we need to stop whatever we're doing, and request the OS to give / free that memory, which slows down the program.

We recommend two simple rules for improving allocation techniques

- Not everything has to be a `List<T>`
    - Whenever possible, if your collections are fixed in size use the `Span<T>` struct along with the `stackalloc` keyword to shift that memory from the heap to the stack.
- Just try to guess
    - Dynamic collections such as `List<T>`, `Dictionary<T>`, `HashSet<T>` spend most of their resources reallocating (growing their capacity), so, we recommend guessing what the final capacity of the collection will be and passing that number to their constructor.

**Non compliant code ❌**
```csharp
public List<char> SplitChars(string input)
{
    var splitResult = new List<char>();
    foreach (char c in input)
    {
        splitResult.Add(c);
    }
    return splitResult;
}
```

**Compliant code ✔️**
```csharp
public List<char> SplitChars(string input)
{
    //Pass in the length of the input as the capacity of the list, this ensures we allocate exactly once
    var splitResult = new List<char>(input.Length);
    foreach (char c in input)
    {
        splitResult.Add(c);
    }
    return splitResult;
}
```

### String concatenation
*"Strings are the root of all evil" - Some C programmer, probably...*

Strings are one of the most difficult data types to work with because of their inherent performance implications; and one of the most common operations is concatenation, however, not all concatenations are born equal, so, let's take a look at some rules.

- Basic concatenation of simple strings with dynamic values
    - If we're concatenating something simple that can be done in one line using the `+` operator, we suggest using C#'s interpolation literal `$` instead which allows us to perform clean concatenations

    **Non compliant code ❌**
    ```csharp
    public void SayName(string name)
    {
        this.logger.Info("Hello there " + name + ", may the force be with you!");
    }
    ```

    **Compliant code ✔️**
    ```csharp
    public void SayName(string name)
    {
        this.logger.Info($"Hello there {name}, may the force be with you!");
    }
    ```
- Concatenation of complex / segmented strings
    - Let's say we have a collection that we need to iterate over and get a string with all their information at the end of the loop, normal concatenation would create a new string instance each time we go around the loop, and strings, being reference types carry a heap allocation each time this happens... So, you can already imagine the performance implications of this type of operations. We suggest using the `StringBuilder` class instead
    
    **Non compliant code ❌**
    ```csharp
    public string GetAccessErrorString(List<HeroRole> roles)
    {
        string errorString = string.Empty;
        foreach (HeroRole role in roles)
        {
            if (KareRoles.IsAdminRole(role.title))
            {
                errorString += $"Role {role.title} does not have admin access\n";
            }
        }
        return errorString;
    }
    ```

    **Compliant code ✔️**
    ```csharp
    public string GetAccessErrorString(List<HeroRole> roles)
    {
        var builder = new StringBuilder();
        foreach (HeroRole role in roles)
        {
            if (KareRoles.IsAdminRole(role.title))
            {
                builer.AppendLine($"Role {role.title} does not have admin access");
            }
        }
        return builder.ToString();
    }
    ```
### Returning multiple values (tuple vs named type)
Always prefer named structs (or `record` if available) instead of tuples.

**Non compliant code ❌**
```csharp
public (List<string> responses, int errorCount) CallExternalApi()
{
    int elementsCount = this.ExternalApiService.GetTotalElements();
    int errorCount = 0;
    var responses = new List<string>(elementsCount); 
    for (int i = 0; i < elementsCount; i++)
    {
        //Http request mock, this is pseudocode
        HttpResponse response = this.ExternalApiService.CallEndpointAt(i);
        if (response.StatusCode != 200)
        {
            errorCount++;
            continue;
        }
        responses.Add(response.Body);
    }
}
```

**Compliant code ✔️**
```csharp
internal struct ExternalApiOperationResults
{
    public List<string> responses; 
    public int errorCount;
}

//Return the names structure instead of the tuple
public ExternalApiOperationResults CallExternalApi()
{
    int elementsCount = this.ExternalApiService.GetTotalElements();
    //Not really needed, but here for demonstration.
    ExternalApiOperationResults result = new ExternalApiOperationResults
    {
        responses = new List<string>(),
        errorCount = 0
    };

    for (int i = 0; i < elementsCount; i++)
    {
        //Http request mock, this is pseudocode
        HttpResponse response = this.ExternalApiService.CallEndpointAt(i);
        if (response.StatusCode != 200)
        {
            result.errorCount++;
            continue;
        }
        result.responses.Add(response.Body);
    }
    return result;
}
```