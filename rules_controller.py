from core.decorators import instance, command, setting
from core.command_param_types import Options, Any, Int, Const, Character
from core.db import DB
from core.text import Text
from core.decorators import instance, command, setting
from core.access_service import AccessService
from core.chat_blob import ChatBlob
from core.tyrbot import Tyrbot
from core.util import Util
from core.lookup.character_service import CharacterService


@instance()
class rulesController:

    def inject(self, registry):
        self.db: DB = registry.get_instance("db")
        self.text: Text = registry.get_instance("text")
        self.bot: Tyrbot = registry.get_instance("bot")
        self.access_service: AccessService = registry.get_instance("access_service")
        self.buddy_service = registry.get_instance ("buddy_service")
        self.character_service: CharacterService = registry.get_instance("character_service")
        self.setting_service: SettingService = registry.get_instance("setting_service")
        self.alts_service: AltsService = registry.get_instance("alts_service")

    
    @command(command="rules", params=[], access_level="all",
             description="Displays the rules")
    def rules_command(self, message):
        rules = self.db.query("SELECT * FROM rules ORDER BY priority, indent, identifier, rule ASC")
        admin_link = self.text.make_chatcmd("admin", "/tell <myname> admins")

        for rule in rules:
            entry = rule.rule
            priority = rule.priority
            indent = rule.indent
            identifier = rule.identifier

            if indent > 0:
                blob += ""
            
            blob += "<header>:: Disclaimer :: <end>\n"
            blob += "The leaders of this bot are free to interpretate the rules in their own way.\n\n"
            blob += "If you feel like one of the leaders is abusing the status, feel free to message an %s.\n\n" % admin_link
 
            blob += "<header>:: Rules  ::<end>\n"

            blob += "%s%s <highlight>%s<end>\n" % (priority, identifier, entry)
            blob += "<pagebreak>"
        
        if rules:
            return ChatBlob("Rules", rules)
        else:
            return "No rules have been set yet."


    @command(command="addrule", params=[Any("rule")], access_level="moderator",
             description="Adds a rule")
    def rules_add_command(self, request, rule: str):
        sql = "INSERT INTO rules (rule, priority, indent) VALUES (?,?,?)"
        count = self.db.exec(sql, [rule, 0, 0])
        
        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully added the new rules entry. Use %s to see an editorial overview of rules." % layoutlink
        else:
            return "Failed to add the new rules entry (DB insertion error)."
    

    @command(command="remrule", params=[Int("rules_id")], access_level="moderator",
             description="Removes a rule")
    def rules_rem_command(self, request, rules_id):            
        sql = "DELETE FROM rules WHERE id = ?";
        count = self.db.exec(sql, [rule_id]);
        
        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully removed the new rules entry. Use %s to see an editorial overview of rules." % layoutlink
        else:
            return "Failed to remove the new rules entry (DB insertion error)."
    

    @command(command="rulepinc", params=[Int("rules_id"), Int("amount")], access_level="moderator",
             description="Removes a rule")
    def rules_pinc_command(self, request, rules_id, amount: int):  
        sql = "UPDATE rules  SET priority = (priority + 1) WHERE id = ?"
        count = self.db.exec(sql, [rule_id])

        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0: 
            return "Successfully changed the priority of rule entry %s. Use %s to see an editorial overview of rules." % (rule_id, layoutlink)
        else:
            return "Failed to change priority of the rule entry (DB update error)."
    
    
    @command(command="rulepdec", params=[Int("rules_id"), Int("amount")], access_level="moderator",
             description="Removes a rule")
    def rules_pdec_command(self, request, rules_id, amount: int):  
        sql = "UPDATE rules SET priority = (priority - 1) WHERE id = ?"
        count = self.db.exec(sql, [rule_id])

        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully changed the priority of rule entry %s. Use %s to see an editorial overview of rules." % (rule_id, layoutlink)
        else:
            return "Failed to change priority of the rule entry (DB update error)."
    

    @command(command="ruleindic", params=[Int("rules_id"), Int("amount")], access_level="moderator",
             description="Removes a rule")
    def rules_indic_command(self, request, rules_id, amount: int): 
        sql = "UPDATE rules SET indent = (indent + 1) WHERE id = ?"
        count = self.db.exec(sql, [rule_id])

        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully changed the indent of rule entry %s. Use %s to see an editorial overview of rules." % (rule_id, layoutlink)
        else:
            return "Failed to change indent of the rule entry (DB update error)."


    @command(command="ruleinddec", params=[Int("rules_id"), Int("amount")], access_level="moderator",
             description="Removes a rule")
    def rules_inddec_command(self, request, rules_id, amount: int): 
        sql = "UPDATE rules SET indent = (indent - 1) WHERE id = ?"
        count = self.db.exec(sql, [rule_id])

        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully changed the indent of rule entry %s. Use %s to see an editorial overview of rules." % (rule_id, layoutlink)
        else:
            return "Failed to change indent of the rule entry (DB update error)."

   
    @command(command="ruleinddec", params=[Int("rules_id"), Int("amount"), Any("word")], access_level="moderator",
             description="Removes a rule")
    def rules_alteridentifier_command(self, request, rules_id, amount: int, word: str):
        sql = "UPDATE rules SET identifier ? WHERE id = ?"
        count = self.db.exec(sql, [identifier, rule_id])

        layoutlink = self.text.make_chatcmd("rules layout", "/tell <myname> ruleslayout")
        
        if count > 0:
            return "Successfully changed the identifier of rule entry %s. Use %s to see an editorial overview of rules." % (rule_id, layoutlink)
        else:
            return "Failed to change identifier of the rule entry (DB update error)." 

    @command(command="ruleinddec", params=[], access_level="moderator",
             description="Removes a rule")
    def rules_layout_command(self, request):
        sql = "SELECT * FROM rules ORDER BY priority, indent, identifier, rule ASC";
        rules = self.db.query(sql);
        
        admin_link = self.text.make_chatcmd("admin", "/tell <myname> admins")   

        for rule in rules:
            entry = rule.rule
            priority = rule.priority
            indent = rule.indent
            identifier = rule.identifier

            if indent > 0:
                blob += ""

        
            incp = self.text.make_chatcmd("p+", "/tell <myname> rulepinc rule_id")
            decp = self.text.make_chatcmd("p-", "/tell <myname> rulepdec rule_id")
            inci = self.text.make_chatcmd("i+", "/tell <myname> ruleindinc rule_id")
            deci = self.text.make_chatcmd("i-", "/tell <myname> ruleinddec rule_id")    
            
            blob += "<header>:: Disclaimer :: <end>\n"
            blob += "The leaders of this bot are free to interpretate the rules in their own way.\n\n"
            blob += "If you feel like one of the leaders is abusing the status, feel free to message an %s.\n\n" % admin_link
  
            blob += "<header>:: Rules  ::<end>\n"

            blob += "%s%s <highlight>%s<end>" % (priority, identifier, entry)
            blob += "(p: %s || i: %s || id: %s)" % (priority, indent, rule_id)
            blob += "[%s] [%s] [%s] [%s]\n" % (incp, decpm, inci, deci)
            blob += "<pagebreak>"

        return ChatBlob("Ruleslayout", ruleslayout)    
        
