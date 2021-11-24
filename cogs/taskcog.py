
from discord.ext import commands,tasks
import datetime as dt
ty=dt.datetime.today().year#今年
def str2day(s):
    """
    文字列を日付に変換
    """
    ns=f"{ty}/"+s
    try:
        tdt = dt.datetime.strptime(ns,"%Y/%m/%d").date()
    except:
        tdt = dt.date.today()+dt.timedelta(weeks=1)
    return tdt


def user_data(ctx):
    """
    与えられたcontextが既存のuserのものならインスタンスを返す
    無ければ作成して返す
    """
    if ctx.author.id not in users:
        usr=user(ctx.author.id,ctx.author)
        users[ctx.author.id]=usr
        return usr
    else:
        return users[ctx.author.id]


users=dict()

class user():
    """
    変数
    UID:ユーザーのID
    name:ユーザー名(かつDMのアドレス)
    tasks:タスクのdict、{ID:task}で管理
    task_num:タスクID設定用のタスク数を保持する変数
    remind:リマインド時間
    done_task:完了したタスク数

    """
    def __init__(self,UID, name):
        self.UID=UID
        self.name=name
        self.tasks=dict()
        self.task_num=1
        self.remind="08:00"
        self.done_task=0


    def add_task(self,contents, day):
        """
        contents(内容)とday(締め切り)からタスクのインスタンスを作成し、
        self.tasksに格納する
        作成したタスクのIDを返す
        """
        tid=self.task_num
        self.tasks[tid]=task(contents,day,self.UID,tid)
        self.task_num+=1
        return tid

    def user_tasks(self):
        """
        self.tasksの中身を出力用文字列にして返す
        """
        out=""
        if len(self.tasks)==0:
            return "task is empty!"
        for tid in self.tasks.keys():
            out+=self.tasks[tid].task_info()
            out+="\n"
        return out

    def remove_task(self,tidst):
        """
        与えられたタスクのIDを削除して出力用文字列を返す
        """
        try:
            tid=int(tidst)
        except:
            return False,"input number!"
        if tid not in self.tasks:
            return False,f"not found taskID : {tid}"
        self.done_task+=1
        return True,"**You did it!**  : "+self.tasks.pop(tid).task_info()+"\n***congrats!***"

    def profile(self):
        """
        プロフィールを返す
        -------------------
        ユーザー名
        今あるタスク
        終わったタスク数
        リマインドする時間
        -------------------
        """
        out=""
        out+=f"name:{self.name}\n"
        out+=f"remaining task:{len(self.tasks)}\n"
        out+=f"finished task:{self.done_task}\n"
        out+=f"remind time:{self.remind}"
        return out

    



    

class task():
    """
    contents:内容
    day     :設定した日付
    user    :発信したユーザー
    task_ID :ユーザーのタスク固有のID

    task_info:タスクの情報を文字列として返す
    """
    def __init__(self, contents, day, user,id):
        self.contents=contents
        self.day=day
        self.user=user
        self.task_ID=id

    def task_info(self):
        return f"{str(self.task_ID).zfill(4)}  :  {self.day.strftime('%m/%d')}  :  {self.contents}"

 

        


class taskcog(commands.Cog,name="task"):
    """
    タスク管理用のコグ
    関数名がそのままコマンドになる

    """

    def __init__(self,bot):
        self.bot=bot

        #リマインダーの時刻をとるためのループをスタートさせる
        self.reminder.start()

    @commands.command(description="add_task")
    async def newtask(self,ctx,contents,day):
        """
        引数として与えられた内容と締め切り日をuserのインスタンスに渡してタスクを追加する
        """
        nd=str2day(day)
        usr=user_data(ctx)
        tid=usr.add_task(contents,nd)
        await ctx.send("added!  :  "+usr.tasks[tid].task_info())
        

    @commands.command(description="task_list")
    async def tasklist(self,ctx):
        """
        今残ってるタスクのリストを表示
        """
        usr=user_data(ctx)
        await ctx.send(usr.user_tasks())

    @commands.command(description="remove_task")
    async def done(self,ctx,tid):
        """
        与えられたIDのタスクを削除し、おめでとうメッセージとリアクションを送信する
        削除に失敗した場合その旨を送信する
        """
        usr=user_data(ctx)
        
        t,s=usr.remove_task(tid)
        if t:
            await ctx.message.add_reaction("\U0001F973")
            await ctx.message.add_reaction("\U0001F44D")
        await ctx.send(s)


    @tasks.loop(seconds=60)
    async def reminder(self):
        """
        リマインダー
        60秒ごとに現在時刻をチェックし
        該当するユーザがいた場合今のタスクのリストをDMに送信する
        """
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
        """
        リマインド時間を設定し、設定完了したことを送信する
        設定できなかった場合はその旨を送信する
        """
        usr=user_data(ctx)
        try:
            dt.datetime.strptime(tim,"%H:%M")
            usr.remind=tim
            print(f"remind_time:{usr.remind}")
            await ctx.send(f"remind time set to {usr.remind}!")
        except:
            await ctx.send("input time(HH:MM)")

    @commands.command(description="profile")
    async def profile(self,ctx):
        """
        プロフィールを送信
        内容はuser.profileを参照
        """
        usr=user_data(ctx)
        await ctx.send(usr.profile())
            


    
            



def setup(bot):
    """
    コグに絶対いるやつ
    """
    print("taskcog OK")
    tc=taskcog(bot)
    return bot.add_cog(tc)