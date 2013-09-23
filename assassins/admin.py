from assassins.models import Player, NewsReport
from django.contrib import admin
from django.core.mail import send_mail

import random

def id_gen(n):
    """id_gen(n): generates a random, n-digit, alpha-numeric key"""
    id_str = ""
    for i in range(0,n):
        id_str += random.choice('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ')
    return id_str

def generate_keys(modeladmin, request, queryset):
    """generates random id keys for each player in the queryset"""
    for player in queryset:
        player.key = id_gen(6)
        player.save()
generate_keys.short_description = "Generate keys for selected players"

def initial_targets(modeladmin, request, queryset):
    """gives all active, living players a new target and guarantees a single 
    loop of player-target relationships"""
    playerlist = list(Player.objects.filter(alive=True, active=True))
    initialplayer = random.choice(playerlist)
    playerlist.remove(initialplayer)
    
    currentplayer = initialplayer
    while len(playerlist) > 0:
        targetplayer = random.choice(playerlist)
        playerlist.remove(targetplayer)

        currentplayer.target = targetplayer
        currentplayer.save()
        currentplayer = targetplayer

    currentplayer.target = initialplayer
    currentplayer.save()
initial_targets.short_description = "Scramble targets for live, active players"

def email_player_info(modeladmin, request, queryset):
    """email all players in the queryset their key and target information"""
    subject = "Assassins is Afoot!"
    for player in queryset:
        message = "Assassins has begun! Listed below is your key and target "
        message+= "information. Keep this information secret, keep it safe.\n "
        message+= "\nYour Key is: " + str(player.key)
        message+= "\nYour Target is: " + str(player.target)
        message+= "\n\nGood luck, and good hunting. Remember, you are being "
        message+= "hunted. \n\nDo not reply to this meesage, send all "
        message+= "questions and concerns to utkhvz@gmail.com"
        
        send_mail(subject, message, 'auto.utkhvz@gmail.com', [player.email])
email_player_info.short_description = "Send email blast to selected players"

def toggle_alive(modeladmin, request, queryset):
    """toggle whether or not each player in the queryset is marked as alive"""
    for player in queryset:
        player.alive = not player.alive
        player.save()
toggle_alive.short_description = "Toggle Alive/Dead for selected players"

def toggle_active(modeladmin, request, queryset):
    """toggle whether or not each player in the queryset is marked as active"""
    for player in queryset:
        player.active = not player.active
        player.save()
toggle_active.short_description = "Toggle Active/Inactive for selected players"

def reset_kills(modeladmin, request, queryset):
    """set the kill count back to 0 for each player in the queryset"""
    for player in queryset:
        player.kills = 0
        player.save()
reset_kills.short_description = "Set selected player kill count back to 0"

def safe_delete(modeladmin, request, queryset):
    """safely unlink and delete players in the queryset"""
    for player in queryset:
        playerlist = Player.objects.exclude(target=None)
        for targeter in playerlist:
            if targeter.target == player:
                targeter.target = None
                targeter.save()
        player.delete()
safe_delete.short_description = "**Safely** delete selected players"
    
# remove the default delete because it breaks things
admin.site.disable_action('delete_selected')

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player', {'fields': ('name', 'email',)}),
        ('Info', {'fields': (('target', 'key', 'kills'),
                             ('active', 'alive', 'career_kills')), 
                  'classes': ('collapse')}),
    ]
    list_display = ('name', 'key', 'kills', 'career_kills', 'target', 
                    'alive', 'active')
    search_fields = ['name', 'key',]
    ordering = ['-active', '-alive', 'name']
    actions = [generate_keys, initial_targets, toggle_alive, toggle_active, 
               safe_delete, reset_kills, email_player_info]
admin.site.register(Player, PlayerAdmin)

class NewsReportAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Report',  {'fields': ('report_type',)}),
        ('Message', {'fields': ('message',)}),
    ]
    list_display = ('__unicode__', 'report_type', 'pub_date')
    ordering = ['-pub_date']
    actions = ['delete_selected']
admin.site.register(NewsReport, NewsReportAdmin)
