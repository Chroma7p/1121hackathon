
from discord.ext import commands,tasks
import datetime as dt
ty=dt.datetime.today().year
def str2day(s):
    ns=f"{ty}/"+s
    try:
        tdt = dt.datetime.strptime(ns,"%Y/%m/%d").date()
    except:
        tdt = dt.date.today()+dt.timedelta(weeks=1)
    return tdt


def user_data(ctx):
    if ctx.author.id not in users:
        usr=user(ctx.author.id,ctx.author)
        users[ctx.author.id]=usr
        return usr
    else:
        return users[ctx.author.id]


users=dict()

class user():
    def __init__(self,UID, name):
        self.UID=UID
        self.name=name
        self.tasks=dict()
        self.task_num=1
        self.remind="08:00"
        self.done_task=0


    def add_task(self,contents, day):
        tid=self.task_num
        self.tasks[tid]=task(contents,day,self.UID,tid)
        self.task_num+=1
        return tid

    def user_tasks(self):
        out=""
        if len(self.tasks)==0:
            return "task is empty!"
        for tid in self.tasks.keys():
            out+=self.tasks[tid].task_info()
            out+="\n"
        return out

    def remove_task(self,tidst):
        try:
            tid=int(tidst)
        except:
            return "input number!"
        if tid not in self.tasks:
            return f"not found taskID:{tid}"
        self.done_task+=1
        return "**You did it!**  : "+self.tasks.pop(tid).task_info()+"\n***congrats!***"

    def profile(self):
        out=""
        out+=f"name:{self.name}\n"
        out+=f"remaining task:{len(self.tasks)}\n"
        out+=f"finished task:{self.done_task}"
        return out

    



    

class task():
    """
    contents:内容
    day     :設定した日付
    user    :発信したユーザー
    task_ID :ユーザーのタスク固有のID
    """
    def __init__(self, contents, day, user,id):
        self.contents=contents
        self.day=day
        self.user=user
        self.task_ID=id

    def task_info(self):
        return f"{str(self.task_ID).zfill(4)}  :  {self.day.strftime('%m/%d')}  :  {self.contents}"

 

        


class taskcog(commands.Cog,name="task"):
    def __init__(self,bot):
        self.bot=bot
        self.reminder.start()
    @commands.command(description="add_task")
    async def newtask(self,ctx,contents,day):
        nd=str2day(day)
        usr=user_data(ctx)
        tid=usr.add_task(contents,nd)
        await ctx.send("added!  :  "+usr.tasks[tid].task_info())
        

    @commands.command(description="task_list")
    async def tasklist(self,ctx):
        usr=user_data(ctx)
        await ctx.send(usr.user_tasks())

    @commands.command(description="remove_task")
    async def done(self,ctx,tid):
        usr=user_data(ctx)
        await ctx.message.add_reaction("\U0001F973")
        await ctx.message.add_reaction("\U0001F44D")
        await ctx.send(usr.remove_task(tid))


    @tasks.loop(seconds=60)
    async def reminder(self):
        now = dt.datetime.now().strftime('%H:%M')
        today =dt.datetime.today().date()
        print(now)
        for uid in users.keys():
            usr=users[uid]
            if now==usr.remind:
                tsks=usr.tasks
                out=f"***{today}  Task REMIND!!!!!***\n"
                
                for tsk in sorted(tsks.values(),key=lambda x:x.day):
                    tid=tsk.task_ID
                    deadline=tsk.day
                    
                    out+=tsks[tid].task_info()
                    if deadline<today:
                        out+="   ***Deadline over!!!***"
                    if deadline==today:
                        out+="   ***Deadline!!!***"
                    out+="\n"
                await usr.name.send(out)

    @commands.command(description="set_remind")
    async def set_remind(self,ctx,tim):
        usr=user_data(ctx)
        try:
            dt.datetime.strptime(tim,"%H:%M")
            usr.remind=tim
            print(f"remind_time:{usr.remind}")
            await ctx.send(f"remind time set to {usr.remind}!")
        except:
            await ctx.send("input time(HH:MM)")

    @commands.command(description="set_remind")
    async def profile(self,ctx):
        usr=user_data(ctx)
        await ctx.send(usr.profile())
            


    
            



def setup(bot):
  print("taskcog OK")
  tc=taskcog(bot)
  return bot.add_cog(tc)