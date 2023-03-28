# Countdown Mastobot 🐘

Mastodon bot for counting down.

**Currently**: counting down to May 12, 2023: the release of [The Legend of Zelda: Tears of the Kingdom](https://www.zelda.com/tears-of-the-kingdom/).

## How to use

I went completely overboard in making what amounts to something that could be done in two lines of Python added to a crontab able to run on a full-fledged kubernetes cluster. BUT, I've made every effort to also make it usable in a crontab setup with minimal fanfare.

### 0: Prerequisites

You'll want to obtain developer / application keys for your bot account first. This is done through your Mastodon instance's web interface, and may depend on what your instance's policies towards bots are. In general, the [botsin.space](https://botsin.space/about) explicitly caters to the design and deployment of bots, though other instances may also be friedly to them.

Specifically, you'll want a `client-key`, `client-secret`, and `access-token` in order to make these scripts work.

### 1: Manually

By "manually", I mean invoking the Python scripts, or maybe the bash script, directly.

You'll need to make sure you have a compatible Python environment. An environment file has been provided so all you need to do is:

 1. Install [conda](https://docs.conda.io/en/latest/) or [mamba](https://mamba.readthedocs.io/en/latest/)
 2. Run `conda create -f environment.yml`

Next, edit the `mastobot.sh` and add your Mastodon credentials to the file (the ones you obtained in "0: Prerequisites" above).

Finally, simply run the bash script:

```
> ./mastobot.sh
```

**Note**: If it fails to run with a "permission denied" error, run `chmod +x mastobot.sh` first, then try the above command again.

### 2: Crontab

You'll still need to go through the process in "1: Manually" of installing and configuring the Python environment for the bot to run in, and modifying the `mastobot.sh` bash script to include the Mastodon credentials for your bot.

After that, you'll run `crontab -e` to bring up the crontab editor. If you've never used cron before, you may want to brush up using [one](https://www.tutorialspoint.com/unix_commands/crontab.htm) [of](https://www.hostinger.com/tutorials/cron-job) [numerous](https://linuxhint.com/cron_jobs_complete_beginners_tutorial/) [tutorials](https://ostechnix.com/a-beginners-guide-to-cron-jobs/) [available](https://linuxconfig.org/using-cron-scheduler-on-linux-systems). Two things to consider:

 1. **Frequency**. The bot is designed to run once per day, though it has provisions to ensure it doesn't happen *more* often than that. So a frequency of something like `0 12 * * *` will run once per day at noon (this is the frequency provided in `mastobot.yaml` for the kubernetes configuration below).
 2. **Command**. This would look something like `/bin/bash /path/to/mastobot.sh` (note the space in there between the `bash` command and the script itself).

### 3: Kubernetes

A full-blown kubernetes deployment is possible with the provided `mastobot.yaml` and `mastobot-credentials.yaml` specifications files.

 - `mastobot.yaml` is the CronJob, which contains information about the frequency of the job, the container image it will pull to run the job, and the environment variables associated with running the job. **You can use this as-is**.
 - `mastobot-credentials.yaml` is the accompanying Secret that contains the Mastodon application credentials. **YOU WILL NEED TO MODIFY THIS.**

Particularly of note: when you receive your Mastodon credentials, but *before* putting them in the Secret, you'll have to run the following command, for *each* of the three values:

```
> echo -n 'client id token in these quotes' | base64
# alonglineofcharacters==
```

You'll run this command three times, one for each of the three values, with the value in the single quotes. It will return another long string of random characters, each with a double equals sign at the end `==`, and it's this *second* string of random characters (including the equals signs!) that you'll put in the `mastobot-credentials.yaml` file.

[See this documentation](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-config-file/) for more details on the process.

Then, you'll run:

```
> kubectl create namespace mastobot
> kubectl apply -f mastobot-credentials.yaml
> kubectl apply -f mastobot.yaml
```

and you're all set!