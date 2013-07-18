from assassins.models import Player
from django.contrib import admin

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
    """gives all living players a new target and guarantees a single loop of 
    player-target relationships"""
    playerlist = list(Player.objects.filter(alive=True))
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
initial_targets.short_description = "Scramble targets for live players"

def toggle_alive(modeladmin, request, queryset):
    """toggle whether or not each player in the queryset is marked as alive"""
    for player in queryset:
        player.alive = not player.alive
        player.save()
toggle_alive.short_description = "Toggle Alive/Dead for selected players"

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player', {'fields': (('name', 'email'), ('key', 'kills', 'alive'))}),
        ('Target', {'fields': ['target'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'alive', 'key', 'kills', 'target')
    search_fields = ['name', 'key']
    ordering = ['-alive', 'name']
    actions = [generate_keys, initial_targets, toggle_alive]

admin.site.register(Player, PlayerAdmin)
