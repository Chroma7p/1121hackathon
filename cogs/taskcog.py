
from discord.ext import commands,tasks
import datetime as dt
ty=dt.datetime.today().year
REMIND_TIME="16:48"

def str2day(s):
    ns=f"{ty}/"+s
    try:
        tdt = dt.datetime.strptime(ns,"%Y/%m/%d").date()
    except:
        tdt = dt.date.today()+dt.timedelta(weeks=1)
    return tdt




users=dict()

class user():
    def __init__(self,UID, name):
        self.UID=UID
        self.name=name
        self.tasks=dict()
        self.task_num=1
        self.remind="08:00"

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
        return "removed! : "+self.tasks.pop(tid).task_info()+"\n***congrats!***"

    



    

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
        uid=ctx.author.id
        if uid not in users:
            usr=user(uid,ctx.author)
            users[uid]=usr
        else:
            usr=users[uid]
        tid=usr.add_task(contents,nd)
        await ctx.send("added!  :  "+usr.tasks[tid].task_info())
        

    @commands.command(description="task_list")
    async def tasklist(self,ctx):
        usr=users[ctx.author.id]
        await ctx.send(usr.user_tasks())

    @commands.command(description="remove_task")
    async def done(self,ctx,tid):
        usr=users[ctx.author.id]
        await ctx.send(usr.remove_task(tid))


    @tasks.loop(seconds=60)
    async def reminder(self):
        
        # 現在の時刻
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
        usr=users[ctx.author.id]
        try:
            dt.datetime.strptime(tim,"%H:%M")
            usr.remind=tim
            print(f"remind_time:{usr.remind}")
            await ctx.send(f"remind time set to {usr.remind}!")
        except:
            await ctx.send("input time(HH:MM)")
            


    
            



def setup(bot):
  print("taskcog OK")
  tc=taskcog(bot)
  return bot.add_cog(tc)