topics_data = [
    {"topic_id": 1, "name": "Budgeting Basics", "min_score": 20},
    {"topic_id": 2, "name": "Saving Strategies", "min_score": 25},
    {"topic_id": 3, "name": "Understanding Credit", "min_score": 30},
    {"topic_id": 4, "name": "Investing Fundamentals", "min_score": 40},
    {"topic_id": 5, "name": "Retirement Planning", "min_score": 35},
    {"topic_id": 6, "name": "Insurance Basics", "min_score": 30},
    {"topic_id": 7, "name": "Taxes and Tax Filing", "min_score": 20},
    {"topic_id": 8, "name": "Debt Management", "min_score": 30},
    {"topic_id": 9, "name": "Home Buying Guide", "min_score": 40},
    {"topic_id": 10, "name": "Financial Goal Setting", "min_score": 15}
]

subtopics_data = [
    # Topic 1: Budgeting Basics
    {"subtopic_id": 1, "topic_id": 1, "name": "Introduction to Budgeting", 
     "content": "Budgeting involves planning your income and expenses to manage finances efficiently. It enables tracking of money flows, allowing one to prioritize essential costs and allocate funds for savings and discretionary spending. "
                "For instance, if monthly earnings are $2000, a budget can allocate $800 for rent, $300 for groceries, $200 for entertainment, and $400 for savings.",
     "quiz": [
         {"question_id": 1, "question": "What is the primary purpose of budgeting?", 
          "options": ["To manage expenses", "To increase income", "To reduce debt"], "correct_option": 0, "points": 5},
         {"question_id": 2, "question": "Which category is not essential for a budget?", 
          "options": ["Savings", "Entertainment", "Rent"], "correct_option": 1, "points": 5},
         {"question_id": 3, "question": "What is one benefit of budgeting?", 
          "options": ["Increased spending", "Improved money management", "High returns"], "correct_option": 1, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 1, "name": "Creating a Budget Plan", 
     "content": "A budget plan outlines income sources and expense categories to track monthly spending. Divide expenses into essentials, savings, and leisure spending. For instance, with a monthly income of $3000, you could allocate "
                "$1500 to fixed costs (e.g., rent, utilities), $500 to savings, and $1000 to discretionary spending.",
     "quiz": [
         {"question_id": 1, "question": "What is a budget plan?", 
          "options": ["An investment strategy", "An income tracker", "A spending allocation tool"], "correct_option": 2, "points": 5},
         {"question_id": 2, "question": "Which is considered a fixed expense?", 
          "options": ["Groceries", "Rent", "Vacation"], "correct_option": 1, "points": 5},
         {"question_id": 3, "question": "What percentage of income is recommended for savings?", 
          "options": ["10%", "20%", "50%"], "correct_option": 1, "points": 10}
     ]},

    # Topic 2: Saving Strategies
    {"subtopic_id": 1, "topic_id": 2, "name": "Introduction to Saving", 
     "content": "Saving is the practice of setting aside a portion of income for future use, often for emergencies or specific goals. For example, by saving $200 monthly from a $2000 income, one can build an emergency fund.",
     "quiz": [
         {"question_id": 1, "question": "What is the main purpose of saving?", 
          "options": ["For emergencies", "For daily expenses", "For debt"], "correct_option": 0, "points": 5},
         {"question_id": 2, "question": "What percentage is typically recommended for savings?", 
          "options": ["5%", "15%", "20%"], "correct_option": 2, "points": 10},
         {"question_id": 3, "question": "Why is an emergency fund important?", 
          "options": ["To spend more", "For unexpected expenses", "For entertainment"], "correct_option": 1, "points": 10}
     ]},
    
    {"subtopic_id": 2, "topic_id": 2, "name": "Types of Savings Accounts", 
     "content": "Different savings accounts serve various needs. A standard savings account offers easy access but lower interest, while high-yield accounts provide more interest. CDs have higher interest but lock funds for a period.",
     "quiz": [
         {"question_id": 1, "question": "Which account has the highest liquidity?", 
          "options": ["Savings", "CD", "IRA"], "correct_option": 0, "points": 5},
         {"question_id": 2, "question": "What is the primary benefit of a CD?", 
          "options": ["High liquidity", "Higher interest rate", "Long-term use"], "correct_option": 1, "points": 5},
         {"question_id": 3, "question": "What account is best for quick access to funds?", 
          "options": ["CD", "High-yield savings", "Investment account"], "correct_option": 1, "points": 10}
     ]},

    # Topic 3: Understanding Credit
    {"subtopic_id": 1, "topic_id": 3, "name": "Credit Basics", 
     "content": "Credit allows borrowing funds now with a promise to repay later, often with interest. Common forms of credit include loans and credit cards. For instance, a credit card purchase paid over time incurs interest.",
     "quiz": [
         {"question_id": 1, "question": "What is credit?", 
          "options": ["Borrowing money", "Investing", "Saving"], "correct_option": 0, "points": 5},
         {"question_id": 2, "question": "What is the cost of borrowing called?", 
          "options": ["Interest", "Dividend", "Principal"], "correct_option": 0, "points": 10},
         {"question_id": 3, "question": "Which is a type of credit?", 
          "options": ["Loan", "Income", "Saving"], "correct_option": 0, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 3, "name": "Understanding Credit Score", 
     "content": "A credit score represents financial reliability, influencing loan eligibility and interest rates. Scores range from 300 to 850, with factors like timely payments affecting it. Higher scores mean lower loan rates.",
     "quiz": [
         {"question_id": 1, "question": "What is a good credit score?", 
          "options": ["300-500", "500-700", "700-850"], "correct_option": 2, "points": 5},
         {"question_id": 2, "question": "Which factor impacts credit score?", 
          "options": ["Income", "Payment history", "Location"], "correct_option": 1, "points": 10},
         {"question_id": 3, "question": "What benefit does a high credit score offer?", 
          "options": ["Lower rates", "More savings", "High income"], "correct_option": 0, "points": 10}
     ]},

    # Topic 4: Investing Fundamentals (Sample Subtopics)
    {"subtopic_id": 1, "topic_id": 4, "name": "Basics of Investing", 
     "content": "Investing is the process of allocating resources, usually money, to generate income or profit. Common investment vehicles include stocks, bonds, and mutual funds. For example, purchasing stocks may offer returns through dividends.",
     "quiz": [
         {"question_id": 1, "question": "What is investing?", 
          "options": ["Earning money", "Allocating money for growth", "Saving in a bank"], "correct_option": 1, "points": 5},
         {"question_id": 2, "question": "What is a common form of investment?", 
          "options": ["Stocks", "Savings", "Income"], "correct_option": 0, "points": 5}
     ]},

    {"subtopic_id": 1, "topic_id": 5, "name": "Introduction to Retirement Planning",
     "content": "Retirement planning involves setting goals for future financial stability once you stop working. It requires calculating future expenses, considering inflation, and saving enough over time to cover these needs.",
     "quiz": [
         {"question_id": 1, "question": "Why is retirement planning important?", 
          "options": ["To prepare for future needs", "To invest in stocks", "To manage current debt"], "correct_option": 0, "points": 5},
         {"question_id": 2, "question": "What is a key factor in retirement planning?", 
          "options": ["Age", "Inflation", "Savings goal"], "correct_option": 2, "points": 10}
     ]},
    
    {"subtopic_id": 2, "topic_id": 5, "name": "Types of Retirement Accounts", 
     "content": "Different retirement accounts help save for the future. A 401(k) is employer-sponsored, while IRAs offer tax advantages. Roth IRAs allow tax-free withdrawals in retirement, which is beneficial for high-income earners.",
     "quiz": [
         {"question_id": 1, "question": "What is a 401(k)?", 
          "options": ["A bank account", "Employer-sponsored retirement plan", "Insurance policy"], "correct_option": 1, "points": 10},
         {"question_id": 2, "question": "Which retirement account offers tax-free withdrawals?", 
          "options": ["Roth IRA", "Traditional IRA", "401(k)"], "correct_option": 0, "points": 10}
     ]},

    # Topic 6: Insurance Basics
    {"subtopic_id": 1, "topic_id": 6, "name": "Understanding Insurance", 
     "content": "Insurance provides financial protection against unexpected losses. Types include health, life, and property insurance. For instance, health insurance covers medical costs, while life insurance provides for beneficiaries upon death.",
     "quiz": [
         {"question_id": 1, "question": "What is the purpose of insurance?", 
          "options": ["To save money", "To invest", "To protect against loss"], "correct_option": 2, "points": 5},
         {"question_id": 2, "question": "Which type of insurance covers medical expenses?", 
          "options": ["Life insurance", "Property insurance", "Health insurance"], "correct_option": 2, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 6, "name": "Types of Insurance", 
     "content": "Various insurance policies serve different needs. Life insurance ensures financial support for beneficiaries, health insurance covers medical expenses, and property insurance protects against property damage or theft.",
     "quiz": [
         {"question_id": 1, "question": "What does property insurance cover?", 
          "options": ["Medical costs", "Death benefits", "Property damage"], "correct_option": 2, "points": 5},
         {"question_id": 2, "question": "Which insurance provides for dependents after one's death?", 
          "options": ["Health", "Life", "Property"], "correct_option": 1, "points": 10}
     ]},

    # Topic 7: Taxes and Tax Filing
    {"subtopic_id": 1, "topic_id": 7, "name": "Basics of Taxation", 
     "content": "Taxes are mandatory contributions to the government, funding public services like healthcare and education. Income tax is a common form, based on annual earnings.",
     "quiz": [
         {"question_id": 1, "question": "What is the primary purpose of taxes?", 
          "options": ["To increase income", "To fund government services", "To reduce inflation"], "correct_option": 1, "points": 5},
         {"question_id": 2, "question": "Which tax is based on annual income?", 
          "options": ["Property tax", "Sales tax", "Income tax"], "correct_option": 2, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 7, "name": "How to File Taxes", 
     "content": "Tax filing involves reporting annual income and calculating owed taxes. Many countries offer online filing, and deductions can reduce taxable income. For example, mortgage interest can be deductible, reducing tax liability.",
     "quiz": [
         {"question_id": 1, "question": "What is tax filing?", 
          "options": ["Paying taxes", "Reporting income to tax authorities", "Calculating deductions"], "correct_option": 1, "points": 10},
         {"question_id": 2, "question": "Which expense is commonly deductible?", 
          "options": ["Groceries", "Mortgage interest", "Entertainment"], "correct_option": 1, "points": 5}
     ]},

    # Topic 8: Debt Management
    {"subtopic_id": 1, "topic_id": 8, "name": "Introduction to Debt", 
     "content": "Debt is borrowed money that must be repaid, typically with interest. Types include credit card debt, student loans, and mortgages. Managing debt ensures that repayments are timely, avoiding high-interest charges.",
     "quiz": [
         {"question_id": 1, "question": "What is debt?", 
          "options": ["Money earned", "Money borrowed", "Money invested"], "correct_option": 1, "points": 5},
         {"question_id": 2, "question": "What is a common form of debt?", 
          "options": ["Savings", "Credit card", "Investments"], "correct_option": 1, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 8, "name": "Strategies for Managing Debt", 
     "content": "Effective debt management strategies include paying more than the minimum, prioritizing high-interest debts, and considering debt consolidation to lower interest rates. Avoiding new debt until current debt is managed is also key.",
     "quiz": [
         {"question_id": 1, "question": "What is debt consolidation?", 
          "options": ["Combining debts into one loan", "Avoiding all debts", "Paying minimum balance"], "correct_option": 0, "points": 10},
         {"question_id": 2, "question": "Why prioritize high-interest debt?", 
          "options": ["To reduce overall interest", "To pay minimum dues", "To save on groceries"], "correct_option": 0, "points": 10}
     ]},

    # Topic 9: Home Buying Guide
    {"subtopic_id": 1, "topic_id": 9, "name": "Steps to Buying a Home", 
     "content": "Buying a home involves assessing finances, obtaining pre-approval, house hunting, making offers, and closing. It’s crucial to save for a down payment and understand mortgage terms.",
     "quiz": [
         {"question_id": 1, "question": "What is the first step in buying a home?", 
          "options": ["House hunting", "Obtaining a mortgage", "Assessing finances"], "correct_option": 2, "points": 10},
         {"question_id": 2, "question": "Why is a down payment important?", 
          "options": ["It reduces loan size", "It lowers taxes", "It increases interest"], "correct_option": 0, "points": 5}
     ]},
    
    {"subtopic_id": 2, "topic_id": 9, "name": "Understanding Mortgages", 
     "content": "A mortgage is a loan to purchase a home, with the property as collateral. Fixed-rate mortgages have a stable interest rate, while adjustable-rate mortgages vary over time.",
     "quiz": [
         {"question_id": 1, "question": "What is a mortgage?", 
          "options": ["A bank account", "A home loan", "A tax incentive"], "correct_option": 1, "points": 5},
         {"question_id": 2, "question": "What is the benefit of a fixed-rate mortgage?", 
          "options": ["Lower taxes", "Stable payments", "More interest"], "correct_option": 1, "points": 5}
     ]},

    # Topic 10: Financial Goal Setting
    {"subtopic_id": 1, "topic_id": 10, "name": "Introduction to Goal Setting",
     "content": "Setting financial goals involves identifying short-term and long-term objectives, such as saving for a car or planning for retirement. It encourages disciplined savings and spending habits.",
     "quiz": [
         {"question_id": 1, "question": "What is the purpose of financial goals?", 
          "options": ["To manage debt", "To encourage savings", "To reduce expenses"], "correct_option": 1, "points": 5},
         {"question_id": 2, "question": "What is a long-term financial goal?", 
          "options": ["Saving for vacation", "Retirement", "Buying groceries"], "correct_option": 1, "points": 10}
     ]},
    
    {"subtopic_id": 2, "topic_id": 10, "name": "Creating a Financial Plan", 
     "content": "A financial plan organizes your income and expenses to meet goals. It includes budgeting, saving, and investing steps to achieve milestones, such as buying a house or funding education.",
     "quiz": [
         {"question_id": 1, "question": "What does a financial plan include?", 
          "options": ["Only budgeting", "Savings and investments", "Entertainment costs only"], "correct_option": 1, "points": 10},
         {"question_id": 2, "question": "What is a benefit of a financial plan?", 
          "options": ["Increased spending", "Achieving financial goals", "Reducing income"], "correct_option": 1, "points": 10}
     ]}
]


from pymongo import MongoClient

# Connect to MongoDB
DATABASE_URL = "mongodb+srv://devansh88karia:wrQ02Ifp0FfTLZB7@cluster0.pzrjg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(DATABASE_URL)
db = client['financeforge']

# Insert topics data into topics collection
topics_collection = db['topics']
topics_collection.insert_many(topics_data)

# Insert subtopics data into subtopics collection
subtopics_collection = db['subtopics']
subtopics_collection.insert_many(subtopics_data)
