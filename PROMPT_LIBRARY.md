# 📚 Prompt Engineering Library

Complete collection of prompts used in this research project. Each strategy is shown with templates and example outputs.

---

## 🎯 Strategy 1: Zero-Shot Prompting

### Definition
Direct instruction without providing examples. The model is asked to complete a task based solely on the instruction.

### Characteristics
- ✅ Simplest to implement
- ✅ Fastest to generate
- ✅ Minimal context
- ❌ Inconsistent output
- ❌ Quality varies

### Template

```
Generate a {DIFFICULTY} level assessment question for {DOMAIN}.

The question should:
- Be clear and unambiguous
- Have a definitive answer
- Be appropriate for {DIFFICULTY} level students

Return ONLY valid JSON (no markdown, no explanation):
{
  "question": "...",
  "answer": "...",
  "difficulty": "{DIFFICULTY}",
  "domain": "{DOMAIN}"
}
```

### Example Outputs

#### Python - Easy
**Question:** What is a variable in Python?  
**Answer:** A variable is a named container that stores a value. You create it by assigning a value using the = operator.

#### JavaScript - Medium
**Question:** What is the difference between 'let' and 'var' in JavaScript?  
**Answer:** 'var' is function-scoped while 'let' is block-scoped. Let also prevents redeclaration in the same scope.

#### SQL - Hard
**Question:** What is a JOIN and when would you use a LEFT JOIN instead of an INNER JOIN?  
**Answer:** A JOIN combines rows from two tables. LEFT JOIN returns all rows from the left table plus matching rows from the right, while INNER JOIN only returns matching rows.

---

## 🔍 Strategy 2: Few-Shot Prompting

### Definition
Providing 2-3 carefully selected examples before asking the model to complete the task. This "primes" the model with the desired format and style.

### Characteristics
- ✅ Better format consistency
- ✅ More predictable output
- ✅ Sets quality expectations
- ✅ Guides answer style
- ❌ Requires more tokens
- ❌ Slightly slower

### Template

```
You are an expert assessment creator specializing in educational content.

EXAMPLE 1 ({DIFFICULTY}, {DOMAIN}):
{
  "question": "[A well-formed question]",
  "answer": "[A comprehensive answer with explanation]",
  "difficulty": "{DIFFICULTY}",
  "domain": "{DOMAIN}"
}

EXAMPLE 2 ({DIFFICULTY}, {DOMAIN}):
{
  "question": "[Another well-formed question]",
  "answer": "[Another comprehensive answer]",
  "difficulty": "{DIFFICULTY}",
  "domain": "{DOMAIN}"
}

Now generate a NEW {DIFFICULTY} level {DOMAIN} question following the exact same format and style.

Requirements:
- Ensure JSON is valid
- Question should be clear and assessable
- Answer should be detailed and educational
- Maintain the same structure as examples
```

### Example Outputs

#### Python - Easy (with examples)
**Question:** What is a Python list and how do you create one?  
**Answer:** A Python list is an ordered, mutable collection of items. You create a list by placing items inside square brackets separated by commas: `my_list = [1, 2, 3, "apple"]`. Lists can contain mixed data types and can be modified after creation.

#### JavaScript - Medium (with examples)
**Question:** Explain the concept of closures in JavaScript and provide a simple example.  
**Answer:** A closure is a function that has access to variables from its outer scope even after that scope has closed. Example:
```javascript
function outer() {
  let count = 0;
  return function inner() {
    count++;
    return count;
  };
}
```
The `inner` function "remembers" the `count` variable.

#### SQL - Hard (with examples)
**Question:** Design a normalized database schema for a library system that tracks books, authors, and borrowing records. Explain your design choices.  
**Answer:** The schema should include:
- `authors` table (id, name, birth_date)
- `books` table (id, title, author_id, isbn, publication_year)
- `members` table (id, name, email, join_date)
- `borrowing_records` table (id, book_id, member_id, borrow_date, return_date)

This design normalizes data, prevents redundancy, and maintains relationships through foreign keys.

---

## 🧠 Strategy 3: Chain-of-Thought Prompting

### Definition
Asking the model to think through the problem step-by-step before generating the final output. This encourages deeper reasoning and more thoughtful responses.

### Characteristics
- ✅ Highest quality output
- ✅ Better reasoning and explanations
- ✅ More nuanced answers
- ✅ Excellent for complex topics
- ✅ Includes reasoning details
- ❌ Uses most tokens
- ❌ Slowest to generate
- ❌ More expensive (if using API)

### Template

```
You are an expert assessment creator with deep knowledge of {DOMAIN}.

Generate a high-quality {DIFFICULTY} level assessment question by following this step-by-step reasoning process:

STEP 1 - Identify the Key Concept:
- What specific concept from {DOMAIN} should this question test?
- Is it foundational ({DIFFICULTY}) or more advanced?
- Ensure it's meaningful and commonly misunderstood

STEP 2 - Consider Learning Objectives:
- What should a student understand after answering this?
- What common misconceptions should this address?
- How does this build on prerequisite knowledge?

STEP 3 - Craft the Question:
- Make the question clear and unambiguous
- Avoid trick questions or unclear wording
- Ensure it requires thought, not just memorization
- End the question with a question mark

STEP 4 - Provide a Comprehensive Answer:
- Include the correct answer
- Add explanation of why this is correct
- Mention common misconceptions to avoid
- Keep answer proportional to question difficulty

STEP 5 - Format and Validate:
- Ensure the question is self-contained
- Verify the answer is complete and accurate
- Check JSON format validity
- Confirm difficulty level appropriateness

Now, output as valid JSON:
{
  "question": "[The complete question]",
  "answer": "[Comprehensive answer with explanation]",
  "reasoning": "[Brief explanation of why this is a good question]",
  "difficulty": "{DIFFICULTY}",
  "domain": "{DOMAIN}"
}
```

### Example Outputs

#### Python - Easy (with reasoning)
**Question:** What will this code print?
```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```

**Answer:** The code will print `[1, 2, 3, 4]`. This is because `y = x` creates a reference to the same list object, not a copy. When you modify `y`, you're modifying the underlying list that both `x` and `y` point to.

**Reasoning:** This question tests understanding of list mutability and the difference between assignment and copying in Python. It addresses a common misconception that assignment creates independent copies.

#### JavaScript - Medium (with reasoning)
**Question:** What is event bubbling in JavaScript? Provide an example of how you would prevent it.

**Answer:** Event bubbling is the process where an event triggered on a child element propagates up through its parent elements. To prevent it, use `event.stopPropagation()`:
```javascript
document.getElementById('child').addEventListener('click', (event) => {
  event.stopPropagation();
  console.log('Child clicked, event won't bubble up');
});
```
You might also use `event.preventDefault()` to prevent default browser behavior.

**Reasoning:** This question tests understanding of the DOM event model, a critical concept for writing effective JavaScript. Developers commonly confuse event bubbling with capturing, so this tests genuine understanding.

#### SQL - Hard (with reasoning)
**Question:** Write a SQL query to find the top 5 customers by total purchase amount in the last 6 months, including their customer ID, name, and total spent. Exclude customers with fewer than 3 purchases.

**Answer:**
```sql
SELECT 
  c.customer_id,
  c.name,
  SUM(o.amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 3
ORDER BY total_spent DESC
LIMIT 5;
```

**Reasoning:** This query tests multiple intermediate SQL skills: JOINs, date filtering, aggregation functions (SUM, COUNT), GROUP BY, HAVING clauses, and sorting. It simulates a real business requirement while being appropriately challenging.

---

## 📊 Comparing the Strategies

### Simple Question Generation

| Strategy | Prompt | Output | Quality |
|----------|--------|--------|---------|
| **Zero-Shot** | "Generate a Python question" | Q: What is a list? A: A list is... | Fair |
| **Few-Shot** | "Here are examples. Generate similar." | Q: What is a list? A: A list is an ordered collection... | Good |
| **Chain-of-Thought** | "Think step-by-step then generate." | Q: What is a list? A: A list is ordered... [detailed reasoning] | Excellent |

### Complex Question Generation

For complex questions (e.g., database design), Chain-of-Thought clearly outperforms other strategies by providing deeper analysis and more comprehensive answers.

---

## 🎯 When to Use Each Strategy

### Use Zero-Shot When:
- You need fast prototyping
- Domain is simple
- Quality variations are acceptable
- Testing MVP concepts
- Example: "Quick Python question generator"

### Use Few-Shot When:
- You need consistent format
- Production system with moderate requirements
- Balancing quality and efficiency
- Resources are somewhat limited
- Example: "Reliable question generator for online courses"

### Use Chain-of-Thought When:
- Quality is critical
- Complex domains with nuance needed
- Need detailed explanations
- High-stakes assessment systems
- Example: "Premium assessment platform"

---

## 💡 Advanced Techniques

### 1. Prompt Chaining
Generate a question with Zero-Shot, then use Few-Shot to refine it:
```
First prompt (Zero-Shot): Generate a question
Second prompt (Few-Shot): Here are good examples. Improve the question.
```

### 2. Temperature Control
- **Lower temperature (0.3-0.5):** More consistent, useful with Few-Shot
- **Higher temperature (0.7-0.9):** More creative, better with Chain-of-Thought

### 3. System Prompts
Add a system message for all strategies:
```
System: "You are an expert education assessment specialist..."
```

---

## 📈 Prompt Engineering Best Practices

1. **Be Specific:** Vague prompts get vague results
2. **Use Delimiters:** Mark examples with `---` or `###`
3. **Specify Format:** Always state "Return JSON" or "Return markdown"
4. **Include Constraints:** Mention difficulty level, length limits
5. **Provide Context:** Help the model understand the use case
6. **Use Role-Playing:** "You are an expert teacher..."
7. **Examples Matter:** Few-Shot dramatically improves quality
8. **Iterate:** Start simple, add complexity gradually

---

**Last Updated:** 2026-06-19  
**Research Complete:** ✅
