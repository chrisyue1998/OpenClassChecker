# OpenClassChecker

This is an AWS Lambda deployment package that checks UMD's Schedule of Classes every minute to determine whether or not a specific class section is open.

How to use:
1. Upload deployment package to AWS Lambda.
2. Add a CloudWatch Events trigger to the Lambda function.
3. Create a new rule for the trigger with the input set as "Constant".
4. Add your class code along with the section number as the keys, add your email or provider's text message email as the values. (ex: {"cmsc389O_0301":"5553324491@txt.att.net", "engl393_9011":"test@gmail.com"})
