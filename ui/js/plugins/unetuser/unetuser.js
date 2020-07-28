define([
    'freeipa/phases',
    'freeipa/ipa'
], function(phases, IPA) {
    function get_item(array, attr, value) {

        for (var i = 0, l = array.length; i < l; i++) {
            if (array[i][attr] === value) return array[i];
        }
        return null;
    }
    var unetuser_plugin = {}
    unetuser_plugin.add_unetuser_preop = function() {
        [IPA.user.entity_spec, IPA.stageuser.stageuser_spec].forEach(function(spec) {
            var facet = get_item(spec.facets, '$type', 'details')
            var section = get_item(facet.sections, 'name', 'identity')
            section.fields.push(
                {
                    name: 'unetid',
                    flags: ['w_if_no_aci'],
                    label: 'Unet ID'
                },
                {
                    name: 'allowunsetreset',
                    flags: ['w_if_no_aci'],
                    label: 'Allow reset using UNET ID?'
                },
                {
                    name: 'sponsor',
                    flags: ['w_if_no_aci'],
                    label: 'Sponsor'   
                },
                {
                    name: 'fwdemail',
                    flags: ['w_if_no_aci'],
                    label: "Forward email?"
                },
                {
                    name: 'expectedgraduation',
                    flags: ['w_if_no_aci'],
                    label: "Expected graduation year"
                }
        )
            
        })
        return true
    }
    phases.on('customization', unetuser_plugin.add_unetuser_preop)

    return unetuser_plugin
})